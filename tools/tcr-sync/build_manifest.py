#!/usr/bin/env python3
"""Build a compact audit manifest for synchronized files.
为已同步文件生成简洁的审计清单。
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 digest of one file. / 返回单个文件的 SHA-256 摘要。"""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: build_manifest.py MIRROR_DIR MAX_HASH_MIB", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    max_hash_bytes = int(sys.argv[2]) * 1024 * 1024
    generated = root / "generated"
    generated.mkdir(parents=True, exist_ok=True)

    records = []
    total_bytes = 0
    skipped_hashes = 0

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == ".git":
            continue
        if relative.as_posix() in {
            "generated/manifest.csv",
            "generated/sync_status.json",
        }:
            continue

        stat = path.stat()
        total_bytes += stat.st_size
        if stat.st_size <= max_hash_bytes:
            digest = sha256(path)
        else:
            digest = "SKIPPED_TOO_LARGE"
            skipped_hashes += 1

        records.append(
            {
                "relative_path": relative.as_posix(),
                "size_bytes": stat.st_size,
                "modified_utc": datetime.fromtimestamp(
                    stat.st_mtime, tz=timezone.utc
                ).isoformat(),
                "sha256": digest,
            }
        )

    with (generated / "manifest.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["relative_path", "size_bytes", "modified_utc", "sha256"],
        )
        writer.writeheader()
        writer.writerows(records)

    status = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "file_count": len(records),
        "total_bytes": total_bytes,
        "hash_skipped_file_count": skipped_hashes,
    }
    (generated / "sync_status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
