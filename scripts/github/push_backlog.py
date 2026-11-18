#!/usr/bin/env python3
"""
push_backlog.py - create the Woad backlog on GitHub from docs/backlog/*.md

Reads docs/backlog/epics.md and docs/backlog/milestone-N.md (the single source of truth)
and uses the GitHub CLI (`gh`) to create:
  * labels (type, area, priority, size, one `milestone:Mx` label per milestone)
  * GitHub milestones (M0 ... M8)
  * one issue per epic, and one issue per backlog item (title: "[M1-06] ...")

Re-running is safe: anything whose Plan ID already appears in an issue title is skipped.

Requirements: Python 3.9+, GitHub CLI (https://cli.github.com), `gh auth login` done.
No third-party Python packages are used.

Examples:
  python scripts/github/push_backlog.py --validate
  python scripts/github/push_backlog.py --repo OWNER/REPO --dry-run
  python scripts/github/push_backlog.py --repo OWNER/REPO --milestones M0,M1
  python scripts/github/push_backlog.py --repo OWNER/REPO --yes
"""
from __future__ import annotations

import argparse
import heapq
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKLOG_DIR = ROOT / "docs" / "backlog"

# ----------------------------------------------------------------------------- label model
TYPE_LABELS = {
    "epic": ("3E4B9E", "Groups the issues of one epic"),
    "feature": ("1D76DB", "New capability"),
    "bug": ("D73A4A", "Defect"),
    "documentation": ("0075CA", "Documentation work"),
    "testing": ("5319E7", "Test infrastructure and tests"),
    "research": ("FBCA04", "Time-boxed spike with written findings"),
    "chore": ("C5DEF5", "Tooling and repository hygiene"),
    "ci": ("BFD4F2", "Continuous integration"),
    "provisional": ("E4E669", "Detail will be revisited before work starts"),
    "good first issue": ("7057FF", "Suitable for a first contribution"),
}
AREAS = ("core", "platform", "graphics", "input", "content", "audio", "collision",
         "diagnostics", "demo", "docs", "build")
AREA_LABELS = {f"area:{a}": ("BFDADC", f"Area: {a}") for a in AREAS}
PRIORITY_LABELS = {
    "P0": ("B60205", "Blocks the milestone"),
    "P1": ("D93F0B", "Important"),
    "P2": ("FBCA04", "Nice to have / first to cut"),
}
SIZE_LABELS = {
    "S": ("C2E0C6", "Up to 3 hours", (0, 3)),
    "M": ("FEF2C0", "3 to 8 hours", (3, 8)),
    "L": ("F9D0C4", "8 to 16 hours", (8, 16)),
}
MILESTONE_COLORS = ["0E8A16", "1D76DB", "5319E7", "FBCA04", "D93F0B",
                    "B60205", "0075CA", "006B75", "BFD4F2", "7057FF"]

KNOWN_ISSUE_LABELS = set(TYPE_LABELS) | set(AREA_LABELS)

ISSUE_ID_RE = re.compile(r"M(\d+)-(\d{2})")
EPIC_ID_RE = re.compile(r"E\d{2}")
META_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.*)$")
TITLE_ID_RE = re.compile(r"^\[((?:M\d+-\d{2})|(?:E\d{2}))\]")


# ----------------------------------------------------------------------------- data model
@dataclass
class Milestone:
    num: int
    name: str
    goal: str
    provisional: bool
    path: Path

    @property
    def key(self) -> str:
        return f"M{self.num}"

    @property
    def title(self) -> str:
        return f"M{self.num} {self.name}"

    @property
    def label(self) -> str:
        return f"milestone:M{self.num}"


@dataclass
class Epic:
    id: str
    name: str
    milestone: str
    labels: list
    priority: str
    goal: str
    outcome: str

    @property
    def title(self) -> str:
        return f"[{self.id}] {self.name}"


@dataclass
class Issue:
    id: str
    name: str
    type: str
    labels: list
    priority: str
    size: str
    hours: float
    epic: str
    depends: list
    description: str
    criteria: list
    milestone: Milestone
    seq: int = 0

    @property
    def title(self) -> str:
        return f"[{self.id}] {self.name}"


# ----------------------------------------------------------------------------- parsing
def parse_meta(line: str) -> dict:
    body = line.strip()
    if body.startswith("- "):
        body = body[2:]
    out = {}
    for part in body.split(" | "):
        m = META_RE.match(part.strip())
        if m:
            out[m.group(1).strip().lower()] = m.group(2).strip()
    return out


def backticked(value: str) -> list:
    return re.findall(r"`([^`]+)`", value)


def parse_milestone_file(path: Path, errors: list):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    head = re.match(r"^# Milestone (\d+): (.+?)(?:\s*\(epics?\s[^)]*\))?\s*$", lines[0] if lines else "")
    if not head:
        errors.append(f"{path.name}: first line must be '# Milestone N: Name (epic Exx)'")
        return None, []
    num = int(head.group(1))
    goal_m = re.search(r"^\*\*Goal:\*\*\s*(.+)$", text, re.M)
    provisional = bool(re.search(r"^\*\*Detail:\*\*\s*provisional", text, re.M | re.I))
    ms = Milestone(num, head.group(2).strip(), goal_m.group(1).strip() if goal_m else "", provisional, path)

    header_idx = [i for i, l in enumerate(lines) if re.match(r"^## M\d+-\d{2} ", l)]
    issues = []
    for n, start in enumerate(header_idx):
        end = header_idx[n + 1] if n + 1 < len(header_idx) else len(lines)
        block = lines[start:end]
        hm = re.match(r"^## (M\d+-\d{2}) (.+)$", block[0])
        iid, name = hm.group(1), hm.group(2).strip()
        meta, depends_line, description, criteria = {}, None, "", []
        in_ac = False
        for l in block[1:]:
            if l.startswith("- **Type:**"):
                meta = parse_meta(l)
                in_ac = False
            elif l.startswith("- **Depends on:**"):
                depends_line = parse_meta(l).get("depends on", "")
                in_ac = False
            elif l.startswith("- **Description:**"):
                description = l[len("- **Description:**"):].strip()
                in_ac = False
            elif l.startswith("- **Acceptance criteria:**"):
                in_ac = True
            elif in_ac:
                m = re.match(r"^\s+- \[ \] (.+)$", l)
                if m:
                    criteria.append(m.group(1).strip())
        if not meta:
            errors.append(f"{iid}: missing '- **Type:** ...' metadata line")
            continue
        size_m = re.match(r"^([SML])\s*\((\d+(?:\.\d+)?)\s*h\)", meta.get("size", ""))
        if not size_m:
            errors.append(f"{iid}: Size must look like 'M (5 h)', got '{meta.get('size', '')}'")
            size, hours = "?", 0.0
        else:
            size, hours = size_m.group(1), float(size_m.group(2))
        depends = ISSUE_ID_RE.findall(depends_line or "")
        depends = [f"M{a}-{b}" for a, b in depends]
        if depends_line is None:
            errors.append(f"{iid}: missing '- **Depends on:**' line (use 'none')")
        issues.append(Issue(
            id=iid, name=name, type=meta.get("type", ""), labels=backticked(meta.get("labels", "")),
            priority=meta.get("priority", ""), size=size, hours=hours, epic=meta.get("epic", ""),
            depends=depends, description=description, criteria=criteria, milestone=ms,
            seq=int(iid.split("-")[1]),
        ))
    return ms, issues


def parse_epics(path: Path, errors: list) -> list:
    lines = path.read_text(encoding="utf-8").splitlines()
    idx = [i for i, l in enumerate(lines) if re.match(r"^## E\d{2} ", l)]
    epics = []
    for n, start in enumerate(idx):
        end = idx[n + 1] if n + 1 < len(idx) else len(lines)
        hm = re.match(r"^## (E\d{2}) (.+)$", lines[start])
        eid, name = hm.group(1), hm.group(2).strip()
        meta, goal, outcome = {}, "", ""
        for l in lines[start + 1:end]:
            if l.startswith("- **Milestone:**"):
                meta = parse_meta(l)
            elif l.startswith("- **Goal:**"):
                goal = l[len("- **Goal:**"):].strip()
            elif l.startswith("- **Outcome:**"):
                outcome = l[len("- **Outcome:**"):].strip()
        if not meta:
            errors.append(f"{eid}: missing '- **Milestone:** ...' metadata line")
            continue
        epics.append(Epic(eid, name, meta.get("milestone", ""), backticked(meta.get("labels", "")),
                          meta.get("priority", ""), goal, outcome))
    return epics


def load_backlog():
    errors = []
    milestones, issues = {}, []
    for path in sorted(BACKLOG_DIR.glob("milestone-*.md")):
        ms, iss = parse_milestone_file(path, errors)
        if ms:
            milestones[ms.key] = ms
            issues.extend(iss)
    epics = parse_epics(BACKLOG_DIR / "epics.md", errors) if (BACKLOG_DIR / "epics.md").exists() else []
    if not epics:
        errors.append("epics.md: no epics found")
    return milestones, epics, issues, errors


# ----------------------------------------------------------------------------- validation
def validate(milestones, epics, issues, errors):
    ids = {}
    epic_ids = {e.id for e in epics}
    for e in epics:
        if e.milestone not in milestones:
            errors.append(f"{e.id}: unknown milestone '{e.milestone}'")
        if e.priority not in PRIORITY_LABELS:
            errors.append(f"{e.id}: bad priority '{e.priority}'")
        for l in e.labels:
            if l not in KNOWN_ISSUE_LABELS:
                errors.append(f"{e.id}: unknown label '{l}'")
    for i in issues:
        if i.id in ids:
            errors.append(f"{i.id}: duplicate ID")
        ids[i.id] = i
        if not i.id.startswith(f"M{i.milestone.num}-"):
            errors.append(f"{i.id}: ID does not match milestone {i.milestone.key} (file {i.milestone.path.name})")
        if i.priority not in PRIORITY_LABELS:
            errors.append(f"{i.id}: priority must be P0, P1 or P2 (got '{i.priority}')")
        if i.size in SIZE_LABELS:
            lo, hi = SIZE_LABELS[i.size][2]
            if not (lo <= i.hours <= hi):
                errors.append(f"{i.id}: size {i.size} must be {lo}-{hi} h but is {i.hours:g} h")
        if i.epic not in epic_ids:
            errors.append(f"{i.id}: unknown epic '{i.epic}'")
        if not i.description:
            errors.append(f"{i.id}: missing description")
        if not i.criteria:
            errors.append(f"{i.id}: needs at least one '  - [ ]' acceptance criterion")
        if not i.labels:
            errors.append(f"{i.id}: no labels")
        for l in i.labels:
            if l not in KNOWN_ISSUE_LABELS:
                errors.append(f"{i.id}: unknown label '{l}'")
    for i in issues:
        for d in i.depends:
            if d not in ids:
                errors.append(f"{i.id}: depends on unknown issue {d}")
            elif d == i.id:
                errors.append(f"{i.id}: depends on itself")
            elif ids[d].milestone.num > i.milestone.num:
                errors.append(f"{i.id}: depends on {d}, which is in a later milestone")
    # cycle check
    try:
        order_issues(issues)
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def order_issues(issues: list) -> list:
    """Dependency-respecting order; ties broken by (milestone, sequence)."""
    by_id = {i.id: i for i in issues}
    indeg = {i.id: 0 for i in issues}
    users = {i.id: [] for i in issues}
    for i in issues:
        for d in i.depends:
            if d in by_id:
                indeg[i.id] += 1
                users[d].append(i.id)
    heap = [(i.milestone.num, i.seq, i.id) for i in issues if indeg[i.id] == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        _, _, iid = heapq.heappop(heap)
        out.append(by_id[iid])
        for u in users[iid]:
            indeg[u] -= 1
            if indeg[u] == 0:
                heapq.heappush(heap, (by_id[u].milestone.num, by_id[u].seq, u))
    if len(out) != len(issues):
        stuck = sorted(set(by_id) - {i.id for i in out})
        raise ValueError("dependency cycle involving: " + ", ".join(stuck[:8]))
    return out


# ----------------------------------------------------------------------------- bodies
LINK_RE = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")


def absolutize(text: str, base_dir: Path, repo: str, branch: str) -> str:
    """Turn relative Markdown links (valid in the repo) into absolute GitHub URLs (valid inside issues)."""
    def fix(m):
        target, _, frag = m.group(1).partition("#")
        try:
            rel = (base_dir / target).resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        return f"](https://github.com/{repo}/blob/{branch}/{rel}{'#' + frag if frag else ''})"
    return LINK_RE.sub(fix, text)


def ref(plan_id: str, nums: dict) -> str:
    return f"#{nums[plan_id]} ({plan_id})" if plan_id in nums else f"{plan_id} (not on GitHub yet)"


def issue_body(i: Issue, epics_by_id: dict, nums: dict, fix=lambda s: s) -> str:
    epic = epics_by_id.get(i.epic)
    epic_txt = ref(i.epic, nums) if epic else i.epic
    lines = [
        f"**Plan ID:** `{i.id}` | **Milestone:** {i.milestone.title} | **Priority:** {i.priority} | "
        f"**Size:** {i.size} ({i.hours:g} h) | **Epic:** {epic_txt}",
        f"**Type:** {i.type}",
        "",
    ]
    if i.milestone.provisional:
        lines += ["> **Provisional:** this item is detailed ahead of time and will be revisited when the "
                  "previous milestone finishes.", ""]
    lines += ["## Description", i.description, "", "## Acceptance criteria"]
    lines += [f"- [ ] {c}" for c in i.criteria]
    lines += ["", "## Dependencies"]
    if i.depends:
        lines.append("Blocked by: " + ", ".join(ref(d, nums) for d in i.depends))
    else:
        lines.append("None.")
    lines += ["", "---",
              f"_Source: `docs/backlog/{i.milestone.path.name}`. Update the plan file and this issue together._"]
    return fix("\n".join(lines) + "\n")


def epic_body(e: Epic, children: list, nums: dict, fix=lambda s: s) -> str:
    lines = [f"**Plan ID:** `{e.id}` | **Priority:** {e.priority}", "",
             "## Goal", e.goal, "", "## Outcome", e.outcome, "", "## Issues"]
    if children:
        for c in children:
            lines.append(f"- [ ] {ref(c.id, nums)} {c.name}" if c.id in nums else f"- [ ] {c.id} {c.name}")
    else:
        lines.append("_No issues selected yet._")
    lines += ["", "---", "_Source: `docs/backlog/epics.md`._"]
    return fix("\n".join(lines) + "\n")


# ----------------------------------------------------------------------------- gh wrapper
class GhError(RuntimeError):
    pass


class Gh:
    def __init__(self, repo: str, dry_run: bool, delay: float):
        self.repo, self.dry_run, self.delay = repo, dry_run, delay
        self.exe = shutil.which("gh")
        self.tmp = tempfile.TemporaryDirectory(prefix="woad-backlog-")
        self._n = 0
        self._last = 0.0

    def run(self, args: list, mutating: bool = True) -> str:
        if self.dry_run:
            return ""
        if not self.exe:
            raise GhError("GitHub CLI 'gh' not found in PATH (https://cli.github.com)")
        if mutating:
            wait = self.delay - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
        for attempt in range(4):
            p = subprocess.run([self.exe] + args, capture_output=True, text=True, encoding="utf-8")
            self._last = time.time()
            if p.returncode == 0:
                return p.stdout
            err = (p.stderr or "").lower()
            if attempt < 3 and ("rate limit" in err or "abuse" in err or "secondary" in err):
                pause = 60 * (attempt + 1)
                say(f"  rate limited; waiting {pause}s ...")
                time.sleep(pause)
                continue
            raise GhError(f"gh {' '.join(args[:4])} ... failed: {(p.stderr or p.stdout).strip()}")
        raise GhError("unreachable")

    def body_file(self, text: str) -> str:
        self._n += 1
        path = Path(self.tmp.name) / f"body{self._n}.md"
        path.write_text(text, encoding="utf-8")
        return str(path)

    # --- read
    def existing_issues(self) -> dict:
        out = self.run(["issue", "list", "--repo", self.repo, "--state", "all", "--limit", "5000",
                        "--json", "number,title"], mutating=False)
        found = {}
        for item in json.loads(out or "[]"):
            m = TITLE_ID_RE.match(item["title"])
            if m:
                found[m.group(1)] = item["number"]
        return found

    def existing_milestones(self) -> dict:
        out = self.run(["api", f"repos/{self.repo}/milestones?state=all&per_page=100", "--paginate",
                        "--jq", ".[] | [.number, .title] | @tsv"], mutating=False)
        found = {}
        for line in out.splitlines():
            if "\t" in line:
                num, title = line.split("\t", 1)
                found[title.strip()] = int(num)
        return found

    # --- write
    def create_label(self, name: str, color: str, desc: str):
        self.run(["label", "create", name, "--repo", self.repo, "--color", color,
                  "--description", desc, "--force"])

    def create_milestone(self, title: str, desc: str):
        self.run(["api", "-X", "POST", f"repos/{self.repo}/milestones", "-f", f"title={title}",
                  "-f", f"description={desc[:900]}"])

    def create_issue(self, title: str, body: str, labels: list, milestone: str) -> int:
        args = ["issue", "create", "--repo", self.repo, "--title", title,
                "--body-file", self.body_file(body), "--milestone", milestone]
        for l in labels:
            args += ["--label", l]
        out = self.run(args)
        url = out.strip().splitlines()[-1]
        return int(url.rstrip("/").rsplit("/", 1)[1])

    def edit_issue_body(self, number: int, body: str):
        self.run(["issue", "edit", str(number), "--repo", self.repo, "--body-file", self.body_file(body)])

    def issue_db_id(self, number: int) -> int:
        return int(self.run(["api", f"repos/{self.repo}/issues/{number}", "--jq", ".id"], mutating=False).strip())

    def add_sub_issue(self, parent: int, child: int):
        self.run(["api", "-X", "POST", f"repos/{self.repo}/issues/{parent}/sub_issues",
                  "-F", f"sub_issue_id={self.issue_db_id(child)}"])

    def add_blocked_by(self, number: int, blocker: int):
        self.run(["api", "-X", "POST", f"repos/{self.repo}/issues/{number}/dependencies/blocked_by",
                  "-F", f"issue_id={self.issue_db_id(blocker)}"])

    def add_to_project(self, owner: str, project_number: str, number: int):
        self.run(["project", "item-add", project_number, "--owner", owner,
                  "--url", f"https://github.com/{self.repo}/issues/{number}"])


def say(msg: str):
    print(msg, flush=True)


# ----------------------------------------------------------------------------- main
def summary_table(milestones, issues):
    say(f"{'Milestone':<34} {'Issues':>6} {'Hours':>7}  Detail")
    for key in sorted(milestones, key=lambda k: milestones[k].num):
        ms = milestones[key]
        its = [i for i in issues if i.milestone.key == key]
        say(f"{ms.title:<34} {len(its):>6} {sum(i.hours for i in its):>7g}  "
            f"{'provisional' if ms.provisional else 'detailed'}")
    say(f"{'Total':<34} {len(issues):>6} {sum(i.hours for i in issues):>7g}")


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Create the Woad backlog on GitHub from docs/backlog/*.md")
    ap.add_argument("--repo", help="OWNER/REPO to create issues in")
    ap.add_argument("--validate", action="store_true", help="parse and validate the backlog files, then exit")
    ap.add_argument("--dry-run", action="store_true", help="print what would be created; no gh calls, works offline")
    ap.add_argument("--milestones", help="comma-separated subset, for example M0,M1 (default: all)")
    ap.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    ap.add_argument("--delay", type=float, default=1.2, help="seconds between write calls (default 1.2)")
    ap.add_argument("--project", metavar="OWNER/NUMBER", help="also add every created issue to this Projects v2 board")
    ap.add_argument("--sub-issues", action="store_true", help="link issues as GitHub sub-issues of their epic (best effort)")
    ap.add_argument("--blocked-by", action="store_true", help="create native 'blocked by' relationships (best effort)")
    ap.add_argument("--branch", default="main", help="branch used for absolute documentation links (default main)")
    ap.add_argument("--relink", action="store_true", help="also refresh the checklist of epics that already exist")
    args = ap.parse_args(argv)

    milestones, epics, issues, errors = load_backlog()
    validate(milestones, epics, issues, errors)
    if errors:
        say("Backlog validation failed:")
        for e in errors:
            say(f"  - {e}")
        return 1
    summary_table(milestones, issues)
    if args.validate:
        say("\nBacklog is valid.")
        return 0
    if not args.repo:
        ap.error("--repo OWNER/REPO is required (or use --validate)")

    wanted = {m.strip().upper() for m in args.milestones.split(",")} if args.milestones else set(milestones)
    unknown = wanted - set(milestones)
    if unknown:
        ap.error(f"unknown milestones: {', '.join(sorted(unknown))}")
    selected = [i for i in issues if i.milestone.key in wanted]
    epics_by_id = {e.id: e for e in epics}
    epic_ids_needed = sorted({i.epic for i in selected})
    sel_milestones = [milestones[k] for k in sorted(wanted, key=lambda k: milestones[k].num)]

    say(f"\nPlan for {args.repo}: {len(sel_milestones)} milestones, {len(epic_ids_needed)} epics, "
        f"{len(selected)} issues{' (DRY RUN)' if args.dry_run else ''}")

    gh = Gh(args.repo, args.dry_run, args.delay)
    fix_epic = lambda s: absolutize(s, BACKLOG_DIR, args.repo, args.branch)
    if not args.dry_run:
        if not gh.exe:
            say("GitHub CLI 'gh' not found. Install it from https://cli.github.com and run 'gh auth login'.")
            return 1
        try:
            gh.run(["auth", "status"], mutating=False)
            gh.run(["repo", "view", args.repo, "--json", "nameWithOwner"], mutating=False)
        except GhError as exc:
            say(f"Cannot use repository {args.repo}: {exc}")
            return 1
        if not args.yes:
            reply = input(f"Create these items in {args.repo}? Type 'yes' to continue: ")
            if reply.strip().lower() != "yes":
                say("Aborted.")
                return 1

    # --- labels
    labels = {}
    labels.update({k: (v[0], v[1]) for k, v in TYPE_LABELS.items()})
    labels.update(AREA_LABELS)
    labels.update({k: v for k, v in PRIORITY_LABELS.items()})
    labels.update({f"size:{k}": (v[0], v[1]) for k, v in SIZE_LABELS.items()})
    for ms in sel_milestones:
        labels[ms.label] = (MILESTONE_COLORS[ms.num % len(MILESTONE_COLORS)], f"Milestone {ms.title}")
    say(f"\nLabels: {len(labels)}")
    for name, (color, desc) in labels.items():
        gh.create_label(name, color, desc)

    # --- milestones
    existing_ms = gh.existing_milestones()
    say("Milestones:")
    for ms in sel_milestones:
        if ms.title in existing_ms:
            say(f"  exists   {ms.title}")
        else:
            say(f"  create   {ms.title}")
            gh.create_milestone(ms.title, ms.goal)

    # --- existing issues
    existing = gh.existing_issues()
    nums = dict(existing)
    fake = [max(list(nums.values()) + [0])]

    def next_number() -> int:
        fake[0] += 1
        return fake[0]

    created_epics, created_children = set(), {}
    # --- epics
    say("\nEpics:")
    first_ms = {e: min((milestones[i.milestone.key].num for i in selected if i.epic == e)) for e in epic_ids_needed}
    for eid in epic_ids_needed:
        e = epics_by_id[eid]
        if eid in nums:
            say(f"  exists   #{nums[eid]} {e.title}")
            continue
        ms = milestones[f"M{first_ms[eid]}"]
        lab = list(dict.fromkeys(e.labels + [e.priority, ms.label]))
        number = next_number() if args.dry_run else gh.create_issue(
            e.title, epic_body(e, [], nums, fix_epic), lab, ms.title)
        nums[eid] = number
        created_epics.add(eid)
        say(f"  created  #{number} {e.title}")

    # --- issues
    say("\nIssues:")
    ordered = order_issues(selected)
    all_ordered = order_issues(issues)
    created = 0
    for n, i in enumerate(ordered, 1):
        if i.id in nums:
            say(f"  [{n:>3}/{len(ordered)}] exists   #{nums[i.id]} {i.title}")
            continue
        lab = list(dict.fromkeys(
            i.labels + [i.priority, f"size:{i.size}", i.milestone.label] + (["provisional"] if i.milestone.provisional else [])))
        body = issue_body(i, epics_by_id, nums, fix_epic)
        number = next_number() if args.dry_run else gh.create_issue(i.title, body, lab, i.milestone.title)
        nums[i.id] = number
        created += 1
        created_children.setdefault(i.epic, []).append(i)
        say(f"  [{n:>3}/{len(ordered)}] created  #{number} {i.title}")

    # --- epic checklists
    say("\nEpic checklists:")
    for eid in epic_ids_needed:
        if eid in created_epics or eid in created_children or args.relink:
            children = [i for i in all_ordered if i.epic == eid and i.id in nums]
            if not args.dry_run:
                gh.edit_issue_body(nums[eid], epic_body(epics_by_id[eid], children, nums, fix_epic))
            say(f"  updated  #{nums[eid]} {epics_by_id[eid].title} ({len(children)} issues)")

    # --- optional extras
    new_ids = {i.id for ch in created_children.values() for i in ch}
    if args.project:
        owner, _, pnum = args.project.partition("/")
        say(f"\nAdding {len(new_ids) + len(created_epics)} items to project {args.project} ...")
        for pid in sorted(created_epics | new_ids):
            try:
                gh.add_to_project(owner, pnum, nums[pid])
            except GhError as exc:
                say(f"  warning: {exc}\n  (needs: gh auth refresh -s project). Skipping project step.")
                break
    if args.sub_issues:
        say("\nLinking sub-issues (best effort) ...")
        try:
            for i in ordered:
                if i.id in new_ids:
                    gh.add_sub_issue(nums[i.epic], nums[i.id])
        except GhError as exc:
            say(f"  warning: sub-issue linking failed and was stopped: {exc}")
    if args.blocked_by:
        say("\nLinking blocked-by relations (best effort) ...")
        try:
            for i in ordered:
                if i.id in new_ids:
                    for d in i.depends:
                        if d in nums:
                            gh.add_blocked_by(nums[i.id], nums[d])
        except GhError as exc:
            say(f"  warning: blocked-by linking failed and was stopped: {exc}")

    say(f"\nDone. Created {len(created_epics)} epics and {created} issues "
        f"({len(selected) - created} already existed)." + (" (dry run, nothing was sent)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except GhError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted. Re-run to continue; existing items are skipped.", file=sys.stderr)
        sys.exit(130)
