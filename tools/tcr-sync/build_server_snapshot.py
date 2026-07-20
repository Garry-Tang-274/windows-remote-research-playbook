#!/usr/bin/env python3
"""Generate a safe directory snapshot without reading file contents.

Outputs under the Git mirror's generated/ directory:
- server_tree.txt
- server_tree.json
- directory_summary.csv
- recent_changes.md

Large research directories are summarized rather than listing every file name.
Symlinks are not followed. Secret-like files and environment files are hidden.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SUMMARY_ONLY_ROOTS = {"data", "embeddings", "models", "archive", "tmp"}
EXCLUDED_DIR_NAMES = {
    ".git",
    ".ssh",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ipynb_checkpoints",
    ".cache",
}
EXCLUDED_FILE_NAMES = {".env"}
EXCLUDED_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
SECRET_NAME_PATTERN = re.compile(
    r"(^|[._-])(password|passwd|token|secret|credential|private[-_]?key)($|[._-])",
    re.IGNORECASE,
)
TREE_DEPTH_DETAILED = 4
TREE_DEPTH_SUMMARY = 2
MAX_TREE_ENTRIES_PER_DIRECTORY = 200
MAX_CHANGE_ITEMS = 200
MAX_SUMMARY_ROWS = 10000


def utc_iso(mtime_ns: int) -> str:
    if not mtime_ns:
        return ""
    return datetime.fromtimestamp(
        mtime_ns / 1_000_000_000, tz=timezone.utc
    ).isoformat()


def human_size(size_bytes: int) -> str:
    value = float(size_bytes)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            if unit == "B":
                return f"{int(value)} B"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size_bytes} B"


def is_sensitive_file(name: str) -> bool:
    lower = name.lower()
    if lower in EXCLUDED_FILE_NAMES or lower.startswith(".env."):
        return True
    if Path(lower).suffix in EXCLUDED_SUFFIXES:
        return True
    return SECRET_NAME_PATTERN.search(lower) is not None


def rel_text(path: Path, root: Path) -> str:
    if path == root:
        return "."
    return path.relative_to(root).as_posix()


def add_stat(
    stats: dict[str, dict[str, int]],
    directory: Path,
    root: Path,
    size_bytes: int,
    mtime_ns: int,
) -> None:
    current = directory
    while True:
        key = rel_text(current, root)
        stats[key]["file_count"] += 1
        stats[key]["total_bytes"] += size_bytes
        stats[key]["latest_mtime_ns"] = max(
            stats[key]["latest_mtime_ns"], mtime_ns
        )
        if current == root:
            break
        current = current.parent


def scan_project(root: Path) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, int]],
    list[str],
]:
    inventory: dict[str, dict[str, Any]] = {}
    directory_stats: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "file_count": 0,
            "directory_count": 0,
            "total_bytes": 0,
            "latest_mtime_ns": 0,
        }
    )
    errors: list[str] = []

    for current_text, dir_names, file_names in os.walk(
        root, topdown=True, followlinks=False
    ):
        current = Path(current_text)
        relative_current = rel_text(current, root)
        parts = () if relative_current == "." else Path(relative_current).parts
        top_name = parts[0] if parts else ""
        summary_mode = top_name in SUMMARY_ONLY_ROOTS

        visible_dirs: list[str] = []
        for name in sorted(dir_names):
            child = current / name
            if name in EXCLUDED_DIR_NAMES:
                continue
            try:
                if child.is_symlink():
                    continue
                child_stat = child.stat()
            except OSError as exc:
                errors.append(f"{child}: {exc}")
                continue

            visible_dirs.append(name)
            child_rel = rel_text(child, root)
            directory_stats[relative_current]["directory_count"] += 1

            child_parts = Path(child_rel).parts
            child_top = child_parts[0] if child_parts else ""
            if child_top not in SUMMARY_ONLY_ROOTS:
                inventory[child_rel] = {
                    "type": "directory",
                    "size_bytes": 0,
                    "mtime_ns": child_stat.st_mtime_ns,
                    "modified_utc": utc_iso(child_stat.st_mtime_ns),
                    "mode": "detailed",
                }

        dir_names[:] = visible_dirs

        for name in sorted(file_names):
            if is_sensitive_file(name):
                continue
            path = current / name
            try:
                if path.is_symlink():
                    continue
                stat = path.stat()
            except OSError as exc:
                errors.append(f"{path}: {exc}")
                continue

            add_stat(
                directory_stats,
                current,
                root,
                stat.st_size,
                stat.st_mtime_ns,
            )

            if not summary_mode:
                path_rel = rel_text(path, root)
                inventory[path_rel] = {
                    "type": "file",
                    "size_bytes": stat.st_size,
                    "mtime_ns": stat.st_mtime_ns,
                    "modified_utc": utc_iso(stat.st_mtime_ns),
                    "mode": "detailed",
                }

    for root_name in sorted(SUMMARY_ONLY_ROOTS):
        root_path = root / root_name
        if not root_path.is_dir():
            continue
        summary = directory_stats.get(root_name, {})
        inventory[root_name] = {
            "type": "directory_summary",
            "size_bytes": int(summary.get("total_bytes", 0)),
            "mtime_ns": int(summary.get("latest_mtime_ns", 0)),
            "modified_utc": utc_iso(int(summary.get("latest_mtime_ns", 0))),
            "file_count": int(summary.get("file_count", 0)),
            "directory_count": int(summary.get("directory_count", 0)),
            "mode": "summary",
        }

        # Keep aggregate change records for the first two levels without
        # exposing every large-data filename.
        prefix = root_name + "/"
        for directory, summary_row in sorted(directory_stats.items()):
            if not directory.startswith(prefix):
                continue
            depth = len(Path(directory).parts)
            if depth > 2:
                continue
            inventory[directory] = {
                "type": "directory_summary",
                "size_bytes": int(summary_row["total_bytes"]),
                "mtime_ns": int(summary_row["latest_mtime_ns"]),
                "modified_utc": utc_iso(int(summary_row["latest_mtime_ns"])),
                "file_count": int(summary_row["file_count"]),
                "directory_count": int(summary_row["directory_count"]),
                "mode": "summary",
            }

    return inventory, dict(directory_stats), errors


def visible_children(path: Path, errors: list[str]) -> list[Path]:
    children: list[Path] = []
    try:
        entries = list(os.scandir(path))
    except OSError as exc:
        errors.append(f"{path}: {exc}")
        return children

    for entry in entries:
        if entry.name in EXCLUDED_DIR_NAMES or is_sensitive_file(entry.name):
            continue
        try:
            if entry.is_symlink():
                continue
        except OSError as exc:
            errors.append(f"{entry.path}: {exc}")
            continue
        children.append(Path(entry.path))

    def sort_key(child: Path) -> tuple[int, str]:
        try:
            is_directory = child.is_dir()
        except OSError:
            is_directory = False
        return (0 if is_directory else 1, child.name.lower())

    return sorted(children, key=sort_key)


def build_tree(
    root: Path,
    directory_stats: dict[str, dict[str, int]],
    errors: list[str],
) -> str:
    lines = [f"{root.name}/"]

    def recurse(path: Path, prefix: str, depth: int, summary_mode: bool) -> None:
        children = visible_children(path, errors)
        if summary_mode:
            children = [child for child in children if child.is_dir()]

        omitted = max(0, len(children) - MAX_TREE_ENTRIES_PER_DIRECTORY)
        shown = children[:MAX_TREE_ENTRIES_PER_DIRECTORY]

        for index, child in enumerate(shown):
            final = index == len(shown) - 1 and omitted == 0
            connector = "└── " if final else "├── "
            next_prefix = prefix + ("    " if final else "│   ")
            child_rel = rel_text(child, root)
            try:
                is_directory = child.is_dir()
            except OSError as exc:
                errors.append(f"{child}: {exc}")
                continue

            if is_directory:
                child_summary_mode = summary_mode or (
                    depth == 0 and child.name in SUMMARY_ONLY_ROOTS
                )
                stat = directory_stats.get(child_rel, {})
                suffix = "/"
                if child_summary_mode:
                    suffix += (
                        f"  [{int(stat.get('file_count', 0))} files, "
                        f"{human_size(int(stat.get('total_bytes', 0)))}]"
                    )
                lines.append(f"{prefix}{connector}{child.name}{suffix}")
                limit = (
                    TREE_DEPTH_SUMMARY
                    if child_summary_mode
                    else TREE_DEPTH_DETAILED
                )
                if depth + 1 < limit:
                    recurse(
                        child,
                        next_prefix,
                        depth + 1,
                        child_summary_mode,
                    )
            elif not summary_mode:
                try:
                    size = child.stat().st_size
                    size_text = human_size(size)
                except OSError:
                    size_text = "unknown"
                lines.append(
                    f"{prefix}{connector}{child.name}  [{size_text}]"
                )

        if summary_mode:
            stat = directory_stats.get(rel_text(path, root), {})
            direct_file_count = 0
            try:
                for entry in os.scandir(path):
                    if entry.name in EXCLUDED_DIR_NAMES or is_sensitive_file(entry.name):
                        continue
                    if entry.is_file(follow_symlinks=False):
                        direct_file_count += 1
            except OSError:
                pass
            if direct_file_count:
                lines.append(
                    f"{prefix}└── [隐藏 {direct_file_count} 个文件名；"
                    f"目录合计 {int(stat.get('file_count', 0))} 个文件]"
                )

        if omitted:
            lines.append(f"{prefix}└── … [{omitted} additional entries omitted]")

    recurse(root, "", 0, False)
    return "\n".join(lines) + "\n"


def compare_inventory(
    previous: dict[str, dict[str, Any]],
    current: dict[str, dict[str, Any]],
) -> tuple[list[str], list[str], list[str]]:
    added = sorted(set(current) - set(previous))
    deleted = sorted(set(previous) - set(current))
    modified: list[str] = []
    comparison_keys = (
        "type",
        "size_bytes",
        "mtime_ns",
        "file_count",
        "directory_count",
    )
    for path in sorted(set(current) & set(previous)):
        before = previous[path]
        after = current[path]
        if any(before.get(key) != after.get(key) for key in comparison_keys):
            modified.append(path)
    return added, modified, deleted


def append_change_section(lines: list[str], title: str, paths: list[str]) -> None:
    lines.extend([f"## {title}", ""])
    if not paths:
        lines.extend(["- 无", ""])
        return
    for path in paths[:MAX_CHANGE_ITEMS]:
        lines.append(f"- `{path}`")
    if len(paths) > MAX_CHANGE_ITEMS:
        lines.append(f"- ……另有 {len(paths) - MAX_CHANGE_ITEMS} 项未展开")
    lines.append("")


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: build_server_snapshot.py SOURCE_DIR OUTPUT_DIR STATE_DIR",
            file=sys.stderr,
        )
        return 2

    source = Path(sys.argv[1]).expanduser().resolve()
    output = Path(sys.argv[2]).expanduser().resolve()
    state_dir = Path(sys.argv[3]).expanduser().resolve()
    if not source.is_dir():
        print(f"source directory does not exist: {source}", file=sys.stderr)
        return 1

    output.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)
    inventory, directory_stats, errors = scan_project(source)
    generated_utc = datetime.now(timezone.utc).isoformat()

    (output / "server_tree.txt").write_text(
        build_tree(source, directory_stats, errors), encoding="utf-8"
    )

    json_payload = {
        "generated_utc": generated_utc,
        "source_root_name": source.name,
        "policy": {
            "summary_only_top_level_directories": sorted(SUMMARY_ONLY_ROOTS),
            "detailed_tree_depth": TREE_DEPTH_DETAILED,
            "summary_tree_depth": TREE_DEPTH_SUMMARY,
            "maximum_entries_per_directory": MAX_TREE_ENTRIES_PER_DIRECTORY,
            "file_contents_read": False,
            "symlinks_followed": False,
            "sensitive_names_hidden": True,
        },
        "inventory": [
            {"relative_path": path, **metadata}
            for path, metadata in sorted(inventory.items())
        ],
        "scan_error_count": len(errors),
        "scan_errors": errors[:100],
    }
    (output / "server_tree.json").write_text(
        json.dumps(json_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary_rows: list[dict[str, Any]] = []
    for directory, stat in sorted(directory_stats.items()):
        depth = 0 if directory == "." else len(Path(directory).parts)
        if depth > 3:
            continue
        summary_rows.append(
            {
                "relative_path": directory,
                "file_count_recursive": int(stat["file_count"]),
                "directory_count_direct": int(stat["directory_count"]),
                "total_bytes_recursive": int(stat["total_bytes"]),
                "latest_modified_utc": utc_iso(int(stat["latest_mtime_ns"])),
            }
        )

    with (output / "directory_summary.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        fieldnames = [
            "relative_path",
            "file_count_recursive",
            "directory_count_direct",
            "total_bytes_recursive",
            "latest_modified_utc",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows[:MAX_SUMMARY_ROWS])

    state_path = state_dir / "server_inventory_state.json"
    previous: dict[str, dict[str, Any]] = {}
    if state_path.exists():
        try:
            previous = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            previous = {}

    added, modified, deleted = compare_inventory(previous, inventory)
    change_lines = [
        "# 服务器项目结构变化",
        "",
        f"- 生成时间：`{generated_utc}`",
        f"- 当前记录项：`{len(inventory)}`",
        f"- 扫描警告：`{len(errors)}`",
        "",
    ]
    if not previous:
        change_lines.extend(
            ["> 首次生成目录快照；当前状态已作为后续比较基线。", ""]
        )
    append_change_section(change_lines, "新增", added)
    append_change_section(change_lines, "修改", modified)
    append_change_section(change_lines, "删除", deleted)
    (output / "recent_changes.md").write_text(
        "\n".join(change_lines), encoding="utf-8"
    )

    state_path.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
