#!/usr/bin/env python3
"""Safely inspect and extract ZIP/TAR archives into a destination directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import tarfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import BinaryIO, Iterable


@dataclass
class Entry:
    path: str
    size: int
    kind: str
    compressed_size: int | None = None


def sha256_path(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def _normalized_relative(name: str) -> PurePosixPath:
    name = name.replace("\\", "/")
    if not name or name.startswith("/") or re.match(r"^[A-Za-z]:/", name):
        raise ValueError(f"unsafe absolute archive path: {name!r}")
    p = PurePosixPath(name)
    if any(part in ("", ".", "..") for part in p.parts):
        raise ValueError(f"unsafe archive path component: {name!r}")
    return p


def _dest_for(root: Path, name: str) -> Path:
    p = _normalized_relative(name)
    out = root.joinpath(*p.parts)
    root_resolved = root.resolve()
    parent_resolved = out.parent.resolve()
    if os.path.commonpath([str(root_resolved), str(parent_resolved)]) != str(root_resolved):
        raise ValueError(f"path escapes destination: {name!r}")
    return out


def _zip_is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def inspect_zip(path: Path, max_ratio: float) -> list[Entry]:
    entries: list[Entry] = []
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            check_name = info.filename.rstrip("/") if info.is_dir() else info.filename
            _normalized_relative(check_name)
            if _zip_is_symlink(info):
                raise ValueError(f"symlink entry rejected: {info.filename}")
            kind = "dir" if info.is_dir() else "file"
            if kind == "file":
                ratio = info.file_size / max(info.compress_size, 1)
                if ratio > max_ratio:
                    raise ValueError(
                        f"suspicious compression ratio {ratio:.1f}x for {info.filename} "
                        f"(limit {max_ratio:.1f}x)"
                    )
            entries.append(Entry(info.filename, info.file_size, kind, info.compress_size))
    return entries


def inspect_tar(path: Path) -> list[Entry]:
    entries: list[Entry] = []
    with tarfile.open(path, "r:*") as tf:
        for m in tf.getmembers():
            check_name = m.name.rstrip("/") if m.isdir() else m.name
            _normalized_relative(check_name)
            if m.issym() or m.islnk():
                raise ValueError(f"link entry rejected: {m.name}")
            if not (m.isfile() or m.isdir()):
                raise ValueError(f"special TAR entry rejected: {m.name}")
            entries.append(Entry(m.name, m.size, "dir" if m.isdir() else "file"))
    return entries


def enforce_limits(entries: Iterable[Entry], max_files: int, max_total: int, max_file: int) -> None:
    files = [e for e in entries if e.kind == "file"]
    if len(files) > max_files:
        raise ValueError(f"archive has {len(files)} files; limit is {max_files}")
    total = sum(e.size for e in files)
    if total > max_total:
        raise ValueError(f"archive expands to {total} bytes; limit is {max_total}")
    oversized = [e for e in files if e.size > max_file]
    if oversized:
        e = max(oversized, key=lambda x: x.size)
        raise ValueError(f"file {e.path!r} is {e.size} bytes; per-file limit is {max_file}")


def _copy(src: BinaryIO, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("wb") as out:
        shutil.copyfileobj(src, out, length=1024 * 1024)


def extract_zip(src: Path, dst: Path) -> None:
    with zipfile.ZipFile(src) as zf:
        for info in zf.infolist():
            name = info.filename.rstrip("/") if info.is_dir() else info.filename
            target = _dest_for(dst, name)
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                if _zip_is_symlink(info):
                    raise ValueError(f"symlink entry rejected: {info.filename}")
                with zf.open(info, "r") as inp:
                    _copy(inp, target)


def extract_tar(src: Path, dst: Path) -> None:
    with tarfile.open(src, "r:*") as tf:
        for m in tf.getmembers():
            target = _dest_for(dst, m.name.rstrip("/") if m.isdir() else m.name)
            if m.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif m.isfile():
                inp = tf.extractfile(m)
                if inp is None:
                    raise ValueError(f"unable to read TAR member: {m.name}")
                with inp:
                    _copy(inp, target)
            else:
                raise ValueError(f"special TAR entry rejected: {m.name}")


def manifest(src: Path, dst: Path, entries: list[Entry]) -> dict:
    files = []
    for e in entries:
        if e.kind != "file":
            continue
        p = _dest_for(dst, e.path)
        files.append({
            "path": e.path,
            "size": p.stat().st_size,
            "sha256": sha256_path(p),
        })
    return {
        "archive": src.name,
        "archive_size": src.stat().st_size,
        "archive_sha256": sha256_path(src),
        "file_count": len(files),
        "total_uncompressed_bytes": sum(f["size"] for f in files),
        "files": files,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archive", type=Path)
    ap.add_argument("destination", type=Path)
    ap.add_argument("--max-files", type=int, default=5000)
    ap.add_argument("--max-total-mb", type=int, default=2048)
    ap.add_argument("--max-file-mb", type=int, default=512)
    ap.add_argument("--max-zip-ratio", type=float, default=200.0)
    ap.add_argument("--manifest", type=Path, default=None)
    args = ap.parse_args()

    src = args.archive.resolve()
    dst = args.destination.resolve()
    if not src.is_file():
        raise SystemExit(f"archive not found: {src}")
    dst.mkdir(parents=True, exist_ok=True)

    if zipfile.is_zipfile(src):
        entries = inspect_zip(src, args.max_zip_ratio)
        kind = "zip"
    elif tarfile.is_tarfile(src):
        entries = inspect_tar(src)
        kind = "tar"
    else:
        raise SystemExit("unsupported archive: expected ZIP or TAR-family file")

    enforce_limits(
        entries,
        max_files=args.max_files,
        max_total=args.max_total_mb * 1024 * 1024,
        max_file=args.max_file_mb * 1024 * 1024,
    )

    if kind == "zip":
        extract_zip(src, dst)
    else:
        extract_tar(src, dst)

    data = manifest(src, dst, entries)
    mf = args.manifest or (dst / "_extraction_manifest.json")
    mf.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
