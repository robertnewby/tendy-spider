#!/usr/bin/env python3
"""Validate Tendy Spider's repository-native project-management dashboard."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "project-management"
RECORD_DIRS = ("milestones", "work-items", "decisions", "risks")
ALLOWED_STATUS = {
    "milestone": {"planned", "ready", "in-progress", "blocked", "review", "done", "deferred"},
    "work-item": {"planned", "ready", "in-progress", "blocked", "review", "done", "deferred"},
    "decision": {"open", "accepted", "superseded", "deferred"},
    "risk": {"open", "mitigated", "accepted", "closed"},
}
ALLOWED_PRIORITY = {"P0", "P1", "P2", "P3"}
ALLOWED_SEVERITY = {"low", "medium", "high", "critical"}
REQUIRED = {
    "milestone": {"type", "id", "project", "title", "status", "priority", "owner_agent", "source_file", "source_status", "updated"},
    "work-item": {"type", "id", "project", "title", "status", "priority", "milestone", "owner_agent", "reviewer_agent", "next_action", "source_file", "updated"},
    "decision": {"type", "id", "project", "title", "status", "priority", "owner_agent", "decision_authority", "next_action", "source_file", "updated"},
    "risk": {"type", "id", "project", "title", "status", "priority", "severity", "owner_agent", "next_action", "source_file", "updated"},
}
BOARD_STATUS = {
    "Planned": "planned",
    "Ready": "ready",
    "In Progress": "in-progress",
    "Blocked": "blocked",
    "Review": "review",
    "Done": "done",
}
PLUGIN_HASHES = {
    "obsidian-tasks-plugin": {
        "main.js": "5c68dd0f4e1838f3bd263df39aa508d66ed94e85cc4a48bb338170be2955e077",
        "manifest.json": "db6fe0eb4f033955cdae3e545a39f69748c87262ea8b352805662c4ccbcb714b",
        "styles.css": "32b3d394b697a058f2dcaef0d38476b3c3e585aea63549a816bcc237cf3e3872",
    },
    "quickadd": {
        "main.js": "a0c59ebed18ab870e7b9dc5f70b84e5730bb15116dba673c8fd6ce90f0aeaf90",
        "manifest.json": "60625157623a60e143aa26ab1823fd10e2361d12b2eb946792a555839231e7d5",
        "styles.css": "7198c40b23c4b1ba825156f376855e6122ed8a7f8792e6bd813ebb86534e133e",
    },
    "obsidian-kanban": {
        "main.js": "a7e3bd4cf25f9b7f53a841c44ce990db0ef5f7954ebcab17ae6dca80310c39ac",
        "manifest.json": "24976787097ead467969e014a35654e7a80e4db49a977689a48afadfa15e1854",
        "styles.css": "ecf6dd31f1727c441cce6f54794b0d3916dcfffc87fa17b855c79ba04a85d9a7",
    },
}


def scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "~"}:
        return ""
    if value == "[]":
        return []
    if value in {"true", "false"}:
        return value == "true"
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc

    result: dict[str, Any] = {}
    current_list: str | None = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_list:
            result[current_list].append(scalar(line[4:]))
            continue
        if line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, raw = line.split(":", 1)
        key = key.strip()
        if raw.strip() == "":
            result[key] = []
            current_list = key
        else:
            result[key] = scalar(raw)
            current_list = None
    return result


def resolve_link(source: Path, target: str) -> Path | None:
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target or "{{" in target:
        return source
    candidates: list[Path] = []
    raw = Path(target)
    if raw.suffix:
        candidates.extend((source.parent / raw, ROOT / raw))
    else:
        candidates.extend(
            (
                source.parent / f"{target}.md",
                ROOT / f"{target}.md",
                source.parent / f"{target}.base",
                ROOT / f"{target}.base",
            )
        )
    return next((candidate.resolve() for candidate in candidates if candidate.exists()), None)


def load_records(errors: list[str]) -> tuple[dict[str, dict[str, Any]], dict[str, Path]]:
    records: dict[str, dict[str, Any]] = {}
    paths: dict[str, Path] = {}
    for directory in RECORD_DIRS:
        for path in sorted((PROJECT_DIR / directory).glob("*.md")):
            try:
                data = frontmatter(path)
            except ValueError as exc:
                errors.append(f"{path.relative_to(ROOT)}: {exc}")
                continue
            record_type = data.get("type")
            if record_type not in REQUIRED:
                errors.append(f"{path.relative_to(ROOT)}: unsupported type {record_type!r}")
                continue
            missing = sorted(key for key in REQUIRED[record_type] if key not in data)
            if missing:
                errors.append(f"{path.relative_to(ROOT)}: missing properties {', '.join(missing)}")
            record_id = str(data.get("id", ""))
            if not record_id:
                errors.append(f"{path.relative_to(ROOT)}: empty id")
                continue
            if record_id in records:
                errors.append(
                    f"duplicate id {record_id}: {paths[record_id].relative_to(ROOT)} and {path.relative_to(ROOT)}"
                )
            records[record_id] = data
            paths[record_id] = path
    return records, paths


def validate_records(
    records: dict[str, dict[str, Any]], paths: dict[str, Path], errors: list[str]
) -> None:
    agent_profiles = {path.stem for path in (ROOT / ".codex" / "agents").glob("*.toml")}
    milestone_ids = {record_id for record_id, data in records.items() if data.get("type") == "milestone"}

    for record_id, data in records.items():
        path = paths[record_id]
        record_type = str(data["type"])
        status = str(data.get("status", ""))
        if data.get("project") != "tendy-spider":
            errors.append(f"{path.relative_to(ROOT)}: project must be tendy-spider")
        if status not in ALLOWED_STATUS[record_type]:
            errors.append(f"{path.relative_to(ROOT)}: invalid status {status!r}")
        priority = data.get("priority")
        if priority not in ALLOWED_PRIORITY:
            errors.append(f"{path.relative_to(ROOT)}: invalid priority {priority!r}")
        owner = data.get("owner_agent")
        if owner not in agent_profiles:
            errors.append(f"{path.relative_to(ROOT)}: unknown owner_agent {owner!r}")
        reviewer = data.get("reviewer_agent")
        if reviewer and reviewer not in agent_profiles:
            errors.append(f"{path.relative_to(ROOT)}: unknown reviewer_agent {reviewer!r}")
        source_file = ROOT / str(data.get("source_file", ""))
        if not source_file.is_file():
            errors.append(f"{path.relative_to(ROOT)}: source_file does not exist")
        updated = str(data.get("updated", ""))
        try:
            updated_date = date.fromisoformat(updated)
            if updated_date > date.today():
                errors.append(f"{path.relative_to(ROOT)}: updated date is in the future")
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: updated must be YYYY-MM-DD")

        if record_type == "work-item":
            if data.get("milestone") not in milestone_ids:
                errors.append(f"{path.relative_to(ROOT)}: unknown milestone {data.get('milestone')!r}")
            dependencies = data.get("depends_on", [])
            if not isinstance(dependencies, list):
                dependencies = [dependencies]
            for dependency in dependencies:
                if dependency not in records:
                    errors.append(f"{path.relative_to(ROOT)}: unknown dependency {dependency!r}")
            if status == "blocked" and not data.get("blocked_reason"):
                errors.append(f"{path.relative_to(ROOT)}: blocked item needs blocked_reason")
            if status == "done" and not data.get("acceptance_evidence"):
                errors.append(f"{path.relative_to(ROOT)}: done item needs acceptance_evidence")

        if record_type == "risk" and data.get("severity") not in ALLOWED_SEVERITY:
            errors.append(f"{path.relative_to(ROOT)}: invalid severity {data.get('severity')!r}")


def validate_source_mirrors(records: dict[str, dict[str, Any]], errors: list[str]) -> None:
    task_text = (ROOT / "TASK.md").read_text(encoding="utf-8")
    task_status: dict[str, str] = {}
    pattern = re.compile(
        r"^## Milestone (\d+) — .+?\n\nStatus: \*\*(.+?)\*\*",
        re.MULTILINE,
    )
    for number, status in pattern.findall(task_text):
        task_status[f"M{number}"] = status.strip().lower()

    milestone_status = {
        record_id: str(data.get("source_status", "")).lower()
        for record_id, data in records.items()
        if data.get("type") == "milestone"
    }
    if task_status != milestone_status:
        errors.append(
            f"milestone mirror differs from TASK.md: expected {task_status}, found {milestone_status}"
        )

    decision_text = (ROOT / "DECISIONS.md").read_text(encoding="utf-8")
    source_decisions = set(re.findall(r"^### (O-\d{3}) —", decision_text, re.MULTILINE))
    dashboard_decisions = {
        record_id for record_id, data in records.items() if data.get("type") == "decision"
    }
    if source_decisions != dashboard_decisions:
        errors.append(
            "open decision mirror differs from DECISIONS.md: "
            f"expected {sorted(source_decisions)}, found {sorted(dashboard_decisions)}"
        )


def validate_board(
    records: dict[str, dict[str, Any]], paths: dict[str, Path], errors: list[str]
) -> None:
    board = PROJECT_DIR / "Boards" / "Delivery Board.md"
    lane: str | None = None
    seen: set[str] = set()
    for line in board.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            lane = line[3:].strip()
            continue
        if lane not in BOARD_STATUS or "[[" not in line:
            continue
        match = re.search(r"\[\[([^]|#]+)", line)
        if not match:
            continue
        linked = resolve_link(board, match.group(1))
        if linked is None:
            errors.append(f"{board.relative_to(ROOT)}: unresolved card link {match.group(1)!r}")
            continue
        try:
            data = frontmatter(linked)
        except ValueError as exc:
            errors.append(f"{linked.relative_to(ROOT)}: {exc}")
            continue
        record_id = str(data.get("id", ""))
        seen.add(record_id)
        expected = BOARD_STATUS[lane]
        if data.get("status") != expected:
            errors.append(
                f"{board.relative_to(ROOT)}: {record_id} is in {lane!r} but status is {data.get('status')!r}"
            )

    work_items = {record_id for record_id, data in records.items() if data.get("type") == "work-item"}
    if work_items != seen:
        errors.append(
            f"delivery board coverage differs from work items: expected {sorted(work_items)}, found {sorted(seen)}"
        )


def validate_links(errors: list[str]) -> None:
    for path in sorted(PROJECT_DIR.rglob("*.md")):
        if "templates" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"!?\[\[([^\]]+)\]\]", text):
            if resolve_link(path, target) is None:
                errors.append(f"{path.relative_to(ROOT)}: unresolved wikilink {target!r}")


def validate_json(errors: list[str]) -> None:
    for path in sorted((ROOT / ".obsidian").rglob("*.json")):
        if path.name == "manifest.json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")


def validate_plugins(errors: list[str]) -> None:
    configured = json.loads(
        (ROOT / ".obsidian" / "community-plugins.json").read_text(encoding="utf-8")
    )
    if set(configured) != set(PLUGIN_HASHES):
        errors.append(
            f"community plugin configuration differs from lock: {configured!r}"
        )
    for plugin_id, files in PLUGIN_HASHES.items():
        for name, expected in files.items():
            path = ROOT / ".obsidian" / "plugins" / plugin_id / name
            if not path.is_file():
                errors.append(f"{path.relative_to(ROOT)}: plugin file is not installed")
                continue
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                errors.append(
                    f"{path.relative_to(ROOT)}: checksum mismatch; expected {expected}, found {actual}"
                )


def main() -> int:
    errors: list[str] = []
    records, paths = load_records(errors)
    validate_records(records, paths, errors)
    validate_source_mirrors(records, errors)
    validate_board(records, paths, errors)
    validate_links(errors)
    validate_json(errors)
    validate_plugins(errors)

    base_text = (PROJECT_DIR / "Project Portfolio.base").read_text(encoding="utf-8")
    if '!file.inFolder("project-management/templates")' not in base_text:
        errors.append("Project Portfolio.base: templates folder must be excluded")
    for view in ("Active Work", "Milestones", "Blocked", "Open Decisions", "Open Risks", "By Agent", "Done"):
        if f"name: {view}" not in base_text:
            errors.append(f"Project Portfolio.base: missing view {view!r}")

    if errors:
        print("Project dashboard validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    counts: dict[str, int] = {}
    for data in records.values():
        record_type = str(data["type"])
        counts[record_type] = counts.get(record_type, 0) + 1
    summary = ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
    print(f"Project dashboard validation passed ({summary}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
