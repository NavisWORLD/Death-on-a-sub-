from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Vault:
    root: Path

    @property
    def manifest(self) -> Path:
        return self.root / "manifest.json"

    @property
    def evidence(self) -> Path:
        return self.root / "evidence"

    @property
    def corpus(self) -> Path:
        return self.root / "corpus"

    @property
    def lessons(self) -> Path:
        return self.root / "lessons" / "family_teaching.jsonl"

    @property
    def heartbeat(self) -> Path:
        return self.root / "heartbeat"

    @property
    def generated(self) -> Path:
        return self.root / "generated"

    @property
    def profile(self) -> Path:
        return self.generated / "profile.json"

    def ensure_layout(self) -> None:
        for path in (
            self.root,
            self.evidence / "text",
            self.evidence / "audio",
            self.evidence / "video",
            self.evidence / "image",
            self.evidence / "other",
            self.corpus,
            self.lessons.parent,
            self.heartbeat,
            self.generated,
        ):
            path.mkdir(parents=True, exist_ok=True)

    def require(self) -> "Vault":
        if not self.manifest.exists():
            raise FileNotFoundError(
                f"{self.root} is not a HEARTLIGHT vault. Run `heartlight init {self.root}` first."
            )
        return self

    def read_manifest(self) -> dict:
        self.require()
        return json.loads(self.manifest.read_text(encoding="utf-8"))


def open_vault(path: str | Path) -> Vault:
    return Vault(Path(path).expanduser().resolve())
