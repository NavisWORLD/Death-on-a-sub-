from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from . import DISCLOSURE
from .models import ArtifactRecord, LessonRecord, ProjectManifest
from .provenance import atomic_write_json, sha256_file, utc_now
from .storage import Vault, open_vault


def init_project(path: str | Path, display_name: str) -> Vault:
    vault = open_vault(path)
    vault.ensure_layout()
    if vault.manifest.exists():
        raise FileExistsError(f"HEARTLIGHT vault already exists: {vault.root}")
    manifest = ProjectManifest(
        schema_version=1,
        display_name=display_name,
        created_at=utc_now(),
        project_id=str(uuid.uuid4()),
        disclosure=DISCLOSURE,
    )
    atomic_write_json(vault.manifest, manifest.to_dict())
    return vault


def _unique_destination(folder: Path, source: Path) -> Path:
    digest = sha256_file(source)[:12]
    safe_name = source.name.replace("/", "_").replace("\\", "_")
    return folder / f"{digest}-{safe_name}"


def ingest_artifact(
    vault_path: str | Path,
    source_path: str | Path,
    *,
    kind: str,
    source: str,
    notes: str = "",
) -> ArtifactRecord:
    vault = open_vault(vault_path).require()
    src = Path(source_path).expanduser().resolve()
    if not src.is_file():
        raise FileNotFoundError(src)
    allowed = {"text", "audio", "video", "image", "other"}
    if kind not in allowed:
        raise ValueError(f"kind must be one of: {', '.join(sorted(allowed))}")

    destination = _unique_destination(vault.evidence / kind, src)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        shutil.copy2(src, destination)

    record = ArtifactRecord(
        artifact_id=str(uuid.uuid4()),
        kind=kind,
        relative_path=str(destination.relative_to(vault.root)).replace("\\", "/"),
        sha256=sha256_file(destination),
        source=source,
        imported_at=utc_now(),
        original_name=src.name,
        notes=notes,
    )
    manifest = vault.read_manifest()
    duplicate = next((a for a in manifest.get("artifacts", []) if a.get("sha256") == record.sha256), None)
    if duplicate is not None:
        return ArtifactRecord(**duplicate)
    manifest.setdefault("artifacts", []).append(record.to_dict())
    atomic_write_json(vault.manifest, manifest)

    if kind == "text":
        corpus_target = vault.corpus / destination.name
        if not corpus_target.exists():
            shutil.copy2(destination, corpus_target)
    return record


def append_lesson(
    vault_path: str | Path,
    *,
    prompt: str,
    response: str,
    teacher: str,
) -> LessonRecord:
    vault = open_vault(vault_path).require()
    if not prompt.strip() or not response.strip() or not teacher.strip():
        raise ValueError("prompt, response, and teacher must not be empty")
    record = LessonRecord(prompt.strip(), response.strip(), teacher.strip(), utc_now())
    vault.lessons.parent.mkdir(parents=True, exist_ok=True)
    with vault.lessons.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
    return record


def _load_lessons(vault: Vault) -> list[dict]:
    if not vault.lessons.exists():
        return []
    lessons: list[dict] = []
    for line in vault.lessons.read_text(encoding="utf-8").splitlines():
        if line.strip():
            lessons.append(json.loads(line))
    return lessons


def build_profile(vault_path: str | Path) -> dict:
    vault = open_vault(vault_path).require()
    manifest = vault.read_manifest()
    heartbeat_path = vault.heartbeat / "signature.json"
    heartbeat = json.loads(heartbeat_path.read_text(encoding="utf-8")) if heartbeat_path.exists() else None
    lessons = _load_lessons(vault)

    text_records: list[dict] = []
    for artifact in manifest.get("artifacts", []):
        if artifact.get("kind") != "text":
            continue
        source_path = vault.root / artifact["relative_path"]
        try:
            text = source_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = source_path.read_text(encoding="utf-8", errors="replace")
        text_records.append(
            {
                "artifact_id": artifact["artifact_id"],
                "source": artifact["source"],
                "sha256": artifact["sha256"],
                "text": text,
            }
        )

    profile = {
        "schema_version": 1,
        "project_id": manifest["project_id"],
        "display_name": manifest["display_name"],
        "built_at": utc_now(),
        "disclosure": DISCLOSURE,
        "behavioral_rules": [
            "Ground claims about the remembered person in supplied evidence or family teaching.",
            "When evidence is missing, say that the archive does not know.",
            "Never claim to be the deceased biological person.",
            "Never claim consciousness, soul, or identity transfer has been proven.",
            "Never pressure a grieving person to continue interacting.",
        ],
        "heartbeat_signature": heartbeat,
        "evidence": manifest.get("artifacts", []),
        "text_corpus": text_records,
        "family_teaching": lessons,
    }
    atomic_write_json(vault.profile, profile)
    return profile
