from __future__ import annotations

import io
import zipfile

from fastapi.testclient import TestClient

from heartlight.home_app import create_app


def test_home_family_flow(tmp_path, monkeypatch):
    monkeypatch.setenv("HEARTLIGHT_HOME_DATA_ROOT", str(tmp_path / "home-data"))
    client = TestClient(create_app())

    assert client.get("/healthz").json()["ok"] is True
    assert client.get("/api/projects").json() == []

    created = client.post("/api/projects", json={"display_name": "Grandma Rose's Lantern"})
    assert created.status_code == 201
    project = created.json()["project"]

    upload = client.post(
        f"/api/projects/{project}/evidence",
        data={"source": "family letters", "notes": "favorite saying"},
        files=[("files", ("letter.txt", b"Always leave room for dessert.", "text/plain"))],
    )
    assert upload.status_code == 201
    assert upload.json()["added"] == 1
    assert upload.json()["records"][0]["original_name"] == "letter.txt"

    lesson = client.post(
        f"/api/projects/{project}/lessons",
        json={
            "teacher": "Mom",
            "prompt": "What did Sunday feel like?",
            "response": "Coffee, records, and everybody talking at once.",
        },
    )
    assert lesson.status_code == 201

    built = client.post(f"/api/projects/{project}/build")
    assert built.status_code == 200
    profile = built.json()
    assert profile["display_name"] == "Grandma Rose's Lantern"
    assert len(profile["evidence"]) == 1
    assert len(profile["family_teaching"]) == 1
    assert "Always leave room for dessert." in profile["text_corpus"][0]["text"]

    status = client.get(f"/api/projects/{project}/status").json()
    assert status["artifacts"] == 1
    assert status["lessons"] == 1
    assert status["profile_built"] is True

    exported = client.get(f"/api/projects/{project}/export")
    assert exported.status_code == 200
    with zipfile.ZipFile(io.BytesIO(exported.content)) as archive:
        names = set(archive.namelist())
    assert "manifest.json" in names
    assert "generated/profile.json" in names

    deleted = client.delete(f"/api/projects/{project}")
    assert deleted.status_code == 200
    assert deleted.json()["deleted"] == project
    assert client.get("/api/projects").json() == []


def test_home_shell_is_pwa_ready(tmp_path, monkeypatch):
    monkeypatch.setenv("HEARTLIGHT_HOME_DATA_ROOT", str(tmp_path / "home-data"))
    client = TestClient(create_app())

    page = client.get("/")
    assert page.status_code == 200
    assert "HEARTLIGHT Home" in page.text
    assert "Drop photos, videos, audio, or text here" in page.text
    assert "Delete Lantern" in page.text

    manifest = client.get("/manifest.webmanifest")
    assert manifest.status_code == 200
    assert manifest.json()["display"] == "standalone"

    worker = client.get("/sw.js")
    assert worker.status_code == 200
    assert "/api/" in worker.text
