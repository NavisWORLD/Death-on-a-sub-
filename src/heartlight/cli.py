from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from .corpus import append_lesson, build_profile, ingest_artifact, init_project
from .heartbeat import analyze_wav
from .provenance import atomic_write_json
from .storage import open_vault


def _print_json(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def cmd_init(args: argparse.Namespace) -> int:
    vault = init_project(args.vault, args.display_name)
    print(f"Created HEARTLIGHT lantern: {vault.root}")
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    record = ingest_artifact(
        args.vault,
        args.path,
        kind=args.kind,
        source=args.source,
        notes=args.notes or "",
    )
    _print_json(record.to_dict())
    return 0


def cmd_heartbeat(args: argparse.Namespace) -> int:
    vault = open_vault(args.vault).require()
    source = Path(args.path).expanduser().resolve()
    signature = analyze_wav(source)
    destination = vault.heartbeat / "source.wav"
    if source != destination:
        shutil.copy2(source, destination)
    atomic_write_json(vault.heartbeat / "signature.json", signature.to_dict())
    _print_json(signature.to_dict())
    return 0


def cmd_teach(args: argparse.Namespace) -> int:
    lesson = append_lesson(
        args.vault,
        prompt=args.prompt,
        response=args.response,
        teacher=args.teacher,
    )
    _print_json(lesson.to_dict())
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    _print_json(build_profile(args.vault))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    vault = open_vault(args.vault).require()
    manifest = vault.read_manifest()
    lessons = 0
    if vault.lessons.exists():
        lessons = sum(1 for line in vault.lessons.read_text(encoding="utf-8").splitlines() if line.strip())
    status = {
        "project_id": manifest["project_id"],
        "display_name": manifest["display_name"],
        "artifacts": len(manifest.get("artifacts", [])),
        "lessons": lessons,
        "heartbeat_signature": (vault.heartbeat / "signature.json").exists(),
        "profile_built": vault.profile.exists(),
        "root": str(vault.root),
    }
    _print_json(status)
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    vault = open_vault(args.vault).require()
    if args.provider == "azure":
        from .cloud.azure import sync_directory
    elif args.provider == "ibm":
        from .cloud.ibm_cos import sync_directory
    else:  # argparse guards this
        raise ValueError(args.provider)
    uploaded = sync_directory(vault.root)
    print(f"Mirrored {uploaded} files to {args.provider}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="heartlight",
        description="HEARTLIGHT // The Lantern Archive",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Create a local memorial vault")
    p.add_argument("vault")
    p.add_argument("--display-name", required=True)
    p.set_defaults(func=cmd_init)

    def add_ingest(name: str, kind: str, help_text: str) -> None:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("vault")
        p.add_argument("path")
        p.add_argument("--source", required=True)
        p.add_argument("--notes")
        p.set_defaults(func=cmd_ingest, kind=kind)

    add_ingest("ingest-text", "text", "Import a text record")
    add_ingest("ingest-audio", "audio", "Import an audio record")
    add_ingest("ingest-video", "video", "Import a video record")
    add_ingest("ingest-image", "image", "Import an image record")
    add_ingest("ingest-media", "other", "Import another media/evidence record")

    p = sub.add_parser("heartbeat", help="Create a rhythm signature from PCM WAV")
    p.add_argument("vault")
    p.add_argument("path")
    p.set_defaults(func=cmd_heartbeat)

    p = sub.add_parser("teach", help="Append a family lesson")
    p.add_argument("vault")
    p.add_argument("--prompt", required=True)
    p.add_argument("--response", required=True)
    p.add_argument("--teacher", required=True)
    p.set_defaults(func=cmd_teach)

    p = sub.add_parser("build", help="Build a grounded memorial profile")
    p.add_argument("vault")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("status", help="Show local vault status")
    p.add_argument("vault")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("sync", help="Mirror vault to an optional cloud provider")
    p.add_argument("vault")
    p.add_argument("--provider", choices=["azure", "ibm"], required=True)
    p.set_defaults(func=cmd_sync)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (ValueError, FileNotFoundError, FileExistsError, RuntimeError) as exc:
        print(f"heartlight: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
