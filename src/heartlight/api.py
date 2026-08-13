from __future__ import annotations

import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Annotated

from .corpus import append_lesson, build_profile, init_project
from .heartbeat import analyze_wav
from .provenance import atomic_write_json
from .storage import open_vault

PROJECT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _data_root() -> Path:
    root = Path(os.environ.get("HEARTLIGHT_DATA_ROOT", "./heartlight-data")).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def _project_path(project: str) -> Path:
    if not PROJECT_RE.fullmatch(project):
        raise ValueError("invalid project identifier")
    return _data_root() / project


def create_app():
    try:
        from fastapi import FastAPI, File, HTTPException, UploadFile
        from pydantic import BaseModel, Field
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("Install server support with: pip install -e '.[server]'") from exc

    app = FastAPI(
        title="HEARTLIGHT API",
        version="0.1.0",
        description="HIP-compatible memorial archive service. Authentication belongs at the gateway or service mesh.",
    )

    class CreateProject(BaseModel):
        project: str = Field(min_length=1, max_length=128)
        display_name: str = Field(min_length=1, max_length=256)

    class Lesson(BaseModel):
        prompt: str = Field(min_length=1, max_length=8000)
        response: str = Field(min_length=1, max_length=32000)
        teacher: str = Field(min_length=1, max_length=256)

    @app.get("/healthz")
    def healthz():
        return {"ok": True, "service": "heartlight", "version": "0.1.0"}

    @app.post("/v1/projects", status_code=201)
    def create_project(body: CreateProject):
        try:
            path = _project_path(body.project)
            vault = init_project(path, body.display_name)
            return {"project": body.project, "root": str(vault.root), "manifest": vault.read_manifest()}
        except (ValueError, FileExistsError) as exc:
            raise HTTPException(status_code=409 if isinstance(exc, FileExistsError) else 400, detail=str(exc)) from exc

    @app.get("/v1/projects/{project}/status")
    def project_status(project: str):
        try:
            vault = open_vault(_project_path(project)).require()
            manifest = vault.read_manifest()
            return {
                "project": project,
                "project_id": manifest["project_id"],
                "display_name": manifest["display_name"],
                "artifacts": len(manifest.get("artifacts", [])),
                "heartbeat_signature": (vault.heartbeat / "signature.json").exists(),
                "profile_built": vault.profile.exists(),
            }
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/v1/projects/{project}/lessons", status_code=201)
    def add_lesson(project: str, body: Lesson):
        try:
            return append_lesson(
                _project_path(project),
                prompt=body.prompt,
                response=body.response,
                teacher=body.teacher,
            ).to_dict()
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/projects/{project}/heartbeat", status_code=201)
    async def upload_heartbeat(project: str, file: Annotated[UploadFile, File()]):
        if file.content_type not in {"audio/wav", "audio/x-wav", "audio/wave", "application/octet-stream"}:
            raise HTTPException(status_code=415, detail="upload an uncompressed PCM WAV file")
        try:
            vault = open_vault(_project_path(project)).require()
            suffix = Path(file.filename or "heartbeat.wav").suffix or ".wav"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                temp_path = Path(tmp.name)
                while chunk := await file.read(1024 * 1024):
                    tmp.write(chunk)
            try:
                signature = analyze_wav(temp_path)
                shutil.copy2(temp_path, vault.heartbeat / "source.wav")
                atomic_write_json(vault.heartbeat / "signature.json", signature.to_dict())
                return signature.to_dict()
            finally:
                temp_path.unlink(missing_ok=True)
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/projects/{project}/build")
    def rebuild(project: str):
        try:
            return build_profile(_project_path(project))
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/v1/projects/{project}/profile")
    def get_profile(project: str):
        try:
            vault = open_vault(_project_path(project)).require()
            if not vault.profile.exists():
                raise HTTPException(status_code=404, detail="profile not built")
            import json
            return json.loads(vault.profile.read_text(encoding="utf-8"))
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app


app = create_app()
