from __future__ import annotations

import shutil
import tempfile
import threading
import webbrowser
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
from starlette.background import BackgroundTask

from .corpus import append_lesson, build_profile, ingest_artifact, init_project
from .heartbeat import analyze_wav
from .home import (
    APP_NAME,
    APP_VERSION,
    HOME_HTML,
    PWA_MANIFEST,
    SERVICE_WORKER,
    _find_port,
    _guess_kind,
    _home_root,
    _list_projects,
    _project_path,
    _slugify,
    _status,
)
from .provenance import atomic_write_json
from .storage import open_vault


class CreateLantern(BaseModel):
    display_name: str = Field(min_length=1, max_length=256)


class Lesson(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)
    response: str = Field(min_length=1, max_length=32000)
    teacher: str = Field(min_length=1, max_length=256)


def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME, version=APP_VERSION, docs_url=None, redoc_url=None)

    @app.get("/", response_class=HTMLResponse)
    def home_page() -> str:
        return HOME_HTML

    @app.get("/manifest.webmanifest")
    def manifest() -> JSONResponse:
        return JSONResponse(PWA_MANIFEST, media_type="application/manifest+json")

    @app.get("/sw.js", response_class=PlainTextResponse)
    def service_worker() -> PlainTextResponse:
        return PlainTextResponse(SERVICE_WORKER, media_type="application/javascript")

    @app.get("/healthz")
    def healthz() -> dict:
        return {"ok": True, "service": "heartlight-home", "version": APP_VERSION}

    @app.get("/api/projects")
    def projects() -> list[dict]:
        return _list_projects()

    @app.post("/api/projects", status_code=201)
    def create_project(body: CreateLantern) -> dict:
        try:
            slug = _slugify(body.display_name)
            vault = init_project(_project_path(slug), body.display_name.strip())
            return {"project": slug, "manifest": vault.read_manifest()}
        except (ValueError, FileExistsError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/api/projects/{project}/status")
    def project_status(project: str) -> dict:
        try:
            return _status(project)
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/api/projects/{project}/evidence", status_code=201)
    async def upload_evidence(
        project: str,
        files: Annotated[list[UploadFile], File()],
        source: Annotated[str, Form()] = "family archive",
        notes: Annotated[str, Form()] = "",
    ) -> dict:
        if not files:
            raise HTTPException(status_code=400, detail="choose at least one file")
        records: list[dict] = []
        for upload in files:
            filename = Path(upload.filename or "memory.bin").name
            with tempfile.NamedTemporaryFile(suffix=Path(filename).suffix, delete=False) as temp:
                temp_path = Path(temp.name)
                while chunk := await upload.read(1024 * 1024):
                    temp.write(chunk)
            try:
                record = ingest_artifact(
                    _project_path(project),
                    temp_path,
                    kind=_guess_kind(filename),
                    source=source.strip() or "family archive",
                    notes=notes.strip(),
                )
                vault = open_vault(_project_path(project)).require()
                manifest_data = vault.read_manifest()
                for item in manifest_data.get("artifacts", []):
                    if item.get("artifact_id") == record.artifact_id:
                        item["original_name"] = filename
                atomic_write_json(vault.manifest, manifest_data)
                records.append(record.to_dict() | {"original_name": filename})
            finally:
                temp_path.unlink(missing_ok=True)
        return {"added": len(records), "records": records}

    @app.post("/api/projects/{project}/heartbeat", status_code=201)
    async def upload_heartbeat(project: str, file: Annotated[UploadFile, File()]) -> dict:
        filename = Path(file.filename or "heartbeat.wav").name
        if Path(filename).suffix.lower() != ".wav":
            raise HTTPException(status_code=415, detail="Choose an uncompressed PCM WAV heartbeat recording")
        try:
            vault = open_vault(_project_path(project)).require()
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
                temp_path = Path(temp.name)
                while chunk := await file.read(1024 * 1024):
                    temp.write(chunk)
            try:
                signature = analyze_wav(temp_path)
                shutil.copy2(temp_path, vault.heartbeat / "source.wav")
                atomic_write_json(vault.heartbeat / "signature.json", signature.to_dict())
                return signature.to_dict()
            finally:
                temp_path.unlink(missing_ok=True)
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/api/projects/{project}/lessons", status_code=201)
    def save_lesson(project: str, body: Lesson) -> dict:
        try:
            return append_lesson(
                _project_path(project),
                prompt=body.prompt,
                response=body.response,
                teacher=body.teacher,
            ).to_dict()
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/api/projects/{project}/build")
    def build(project: str) -> dict:
        try:
            return build_profile(_project_path(project))
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/projects/{project}/export")
    def export(project: str) -> FileResponse:
        try:
            vault = open_vault(_project_path(project)).require()
            temp_dir = Path(tempfile.mkdtemp(prefix="heartlight-export-"))
            target = temp_dir / f"{project}-heartlight-backup"
            archive = Path(shutil.make_archive(str(target), "zip", vault.root))
            return FileResponse(
                archive,
                filename=f"{project}-HEARTLIGHT-backup.zip",
                media_type="application/zip",
                background=BackgroundTask(shutil.rmtree, temp_dir, True),
            )
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app


def main() -> int:
    _home_root()
    port = _find_port()
    url = f"http://127.0.0.1:{port}/"
    threading.Timer(0.9, lambda: webbrowser.open(url)).start()
    uvicorn.run(create_app(), host="127.0.0.1", port=port, log_level="warning", access_log=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
