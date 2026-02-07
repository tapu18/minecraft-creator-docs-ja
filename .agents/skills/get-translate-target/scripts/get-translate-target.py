#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import glob
import json
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class TargetsConfig:
    upstream_dir: str
    output_dir: str
    include: List[str]
    exclude: List[str]


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def _parse_targets_fallback(path: str) -> TargetsConfig:
    base: Dict[str, str] = {}
    include: List[str] = []
    exclude: List[str] = []
    section = ""

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            if line == "base:":
                section = "base"
                continue
            if line == "include:":
                section = "include"
                continue
            if line == "exclude:":
                section = "exclude"
                continue
            if line == "priorities:":
                section = "priorities"
                continue

            if section == "base":
                if ":" in line:
                    key, value = line.split(":", 1)
                    base[key.strip()] = value.strip().strip('"')
                continue

            if section in {"include", "exclude"}:
                if line.startswith("-"):
                    value = line.lstrip("-").strip().strip('"')
                    if section == "include":
                        include.append(value)
                    else:
                        exclude.append(value)

    return TargetsConfig(
        upstream_dir=base.get("upstream_dir", ""),
        output_dir=base.get("output_dir", ""),
        include=include,
        exclude=exclude,
    )


def load_targets(path: str) -> TargetsConfig:
    try:
        import yaml  # type: ignore
    except Exception:
        return _parse_targets_fallback(path)

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    base = data.get("base", {}) or {}
    include = data.get("include", []) or []
    exclude = data.get("exclude", []) or []
    return TargetsConfig(
        upstream_dir=base.get("upstream_dir", ""),
        output_dir=base.get("output_dir", ""),
        include=list(include),
        exclude=list(exclude),
    )


def is_excluded(relative_path: str, patterns: List[str]) -> bool:
    rel = _normalize_path(relative_path)
    for raw in patterns:
        pattern = _normalize_path(raw).replace("**", "*")
        if fnmatch.fnmatch(rel, pattern):
            return True
    return False


def get_include_files(root: str, patterns: List[str]) -> List[str]:
    results: List[str] = []
    seen = set()
    for raw in patterns:
        pattern = _normalize_path(raw)
        if "**" in pattern:
            base = pattern.replace("/**", "")
            dir_path = os.path.join(root, base)
            if os.path.isdir(dir_path):
                for file_path in glob.glob(
                    os.path.join(dir_path, "**", "*"), recursive=True
                ):
                    if os.path.isfile(file_path) and file_path not in seen:
                        seen.add(file_path)
                        results.append(file_path)
        else:
            path = os.path.join(root, pattern)
            for file_path in glob.glob(path):
                if os.path.isfile(file_path) and file_path not in seen:
                    seen.add(file_path)
                    results.append(file_path)
    return results


def find_targets(
    upstream_root: str, output_root: str, include: List[str], exclude: List[str]
) -> Tuple[List[str], List[str]]:
    files = get_include_files(upstream_root, include)
    missing: List[str] = []
    outdated: List[str] = []

    for file_path in files:
        relative = os.path.relpath(file_path, upstream_root)
        if is_excluded(relative, exclude):
            continue

        translated_path = os.path.join(output_root, relative)
        if not os.path.exists(translated_path):
            missing.append(_normalize_path(relative))
            continue

        src_mtime = os.path.getmtime(file_path)
        dst_mtime = os.path.getmtime(translated_path)
        if src_mtime > dst_mtime:
            outdated.append(_normalize_path(relative))

    return sorted(missing), sorted(outdated)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List missing and outdated translation targets."
    )
    parser.add_argument(
        "--targets-path",
        default="translation-assets/targets.yml",
        help="Path to translation-assets/targets.yml",
    )
    parser.add_argument(
        "--upstream-root",
        default="",
        help="Override base.upstream_dir from targets.yml",
    )
    parser.add_argument(
        "--output-root",
        default="",
        help="Override base.output_dir from targets.yml",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of text",
    )
    parser.add_argument(
        "--out-file",
        default="",
        help="Write output to a file path",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    config = load_targets(args.targets_path)
    upstream_root = args.upstream_root or config.upstream_dir
    output_root = args.output_root or config.output_dir

    if not upstream_root or not output_root:
        print(
            f"Missing base.upstream_dir or base.output_dir in {args.targets_path}",
            file=sys.stderr,
        )
        return 1

    upstream_full = os.path.abspath(upstream_root)
    output_full = os.path.abspath(output_root)

    missing, outdated = find_targets(
        upstream_full, output_full, config.include, config.exclude
    )

    if args.json:
        payload = {
            "missing": missing,
            "outdated": outdated,
            "counts": {"missing": len(missing), "outdated": len(outdated)},
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        lines = [f"Missing: {len(missing)}"]
        lines.extend([f"  - {item}" for item in missing])
        lines.append("")
        lines.append(f"Outdated: {len(outdated)}")
        lines.extend([f"  - {item}" for item in outdated])
        text = "\n".join(lines)

    if args.out_file:
        with open(args.out_file, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
