from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ArtifactRecord:
    artifact_id: str
    kind: str
    relative_path: str
    sha256: str
    source: str
    imported_at: str
    original_name: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LessonRecord:
    prompt: str
    response: str
    teacher: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class HeartbeatSignature:
    source_sha256: str
    sample_rate: int
    duration_seconds: float
    beat_times_seconds: list[float]
    intervals_seconds: list[float]
    estimated_bpm: float | None
    rhythm_digest: str
    algorithm: str = "heartlight-envelope-peaks-v1"
    caveat: str = (
        "Signal-derived memorial rhythm only; not a medical interpretation, biometric identity, "
        "or evidence of consciousness continuity."
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ProjectManifest:
    schema_version: int
    display_name: str
    created_at: str
    project_id: str
    disclosure: str
    artifacts: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
