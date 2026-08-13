from __future__ import annotations

import json
import os
import platform
import re
import shutil
import socket
import tempfile
import threading
import webbrowser
from pathlib import Path
from typing import Annotated

from .corpus import append_lesson, build_profile, ingest_artifact, init_project
from .heartbeat import analyze_wav
from .provenance import atomic_write_json
from .storage import open_vault

APP_NAME = "HEARTLIGHT Home"
APP_VERSION = "0.2.0"
PROJECT_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,80}$")


def _default_home_root() -> Path:
    override = os.environ.get("HEARTLIGHT_HOME_DATA_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    system = platform.system().lower()
    home = Path.home()
    if system == "windows":
        base = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
        return base / "HEARTLIGHT"
    if system == "darwin":
        return home / "Library" / "Application Support" / "HEARTLIGHT"
    return Path(os.environ.get("XDG_DATA_HOME", home / ".local" / "share")) / "heartlight"


def _home_root() -> Path:
    root = _default_home_root()
    root.mkdir(parents=True, exist_ok=True)
    return root


def _slugify(value: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    base = base[:48] or "lantern"
    candidate = base
    index = 2
    while (_home_root() / candidate).exists():
        candidate = f"{base}-{index}"
        index += 1
    return candidate


def _project_path(project: str) -> Path:
    if not PROJECT_RE.fullmatch(project):
        raise ValueError("invalid lantern identifier")
    path = (_home_root() / project).resolve()
    if _home_root() not in path.parents:
        raise ValueError("invalid lantern path")
    return path


def _guess_kind(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".txt", ".md", ".csv", ".json", ".rtf"}:
        return "text"
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".tif", ".tiff"}:
        return "image"
    if suffix in {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"}:
        return "audio"
    if suffix in {".mp4", ".mov", ".m4v", ".avi", ".webm", ".mkv"}:
        return "video"
    return "other"


def _status(project: str) -> dict:
    vault = open_vault(_project_path(project)).require()
    manifest = vault.read_manifest()
    lessons = 0
    if vault.lessons.exists():
        lessons = sum(1 for line in vault.lessons.read_text(encoding="utf-8").splitlines() if line.strip())
    return {
        "project": project,
        "project_id": manifest["project_id"],
        "display_name": manifest["display_name"],
        "artifacts": len(manifest.get("artifacts", [])),
        "lessons": lessons,
        "heartbeat_signature": (vault.heartbeat / "signature.json").exists(),
        "profile_built": vault.profile.exists(),
        "root": str(vault.root),
    }


def _list_projects() -> list[dict]:
    projects: list[dict] = []
    for child in sorted(_home_root().iterdir()):
        if not child.is_dir() or not (child / "manifest.json").exists():
            continue
        try:
            projects.append(_status(child.name))
        except (ValueError, FileNotFoundError, json.JSONDecodeError):
            continue
    return projects


HOME_HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
<meta name="theme-color" content="#171523" />
<link rel="manifest" href="/manifest.webmanifest" />
<title>HEARTLIGHT Home</title>
<style>
:root{color-scheme:dark;--bg:#0f0e17;--panel:#191725;--soft:#242136;--text:#fffaf2;--muted:#bcb6ca;--pink:#ff8fcf;--gold:#ffd98d;--mint:#99f0cf;--line:#39344c;--danger:#ff9aa8}
*{box-sizing:border-box}body{margin:0;font-family:ui-rounded,"SF Pro Rounded",Inter,system-ui,sans-serif;background:radial-gradient(circle at 20% 0,#282042 0,#0f0e17 40%);color:var(--text);min-height:100vh}.shell{max-width:1100px;margin:auto;padding:24px}.hero{display:flex;gap:18px;align-items:center;margin:8px 0 26px}.orb{width:76px;height:76px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0 4%,var(--pink) 8%,#6d4ef7 44%,#171523 70%);box-shadow:0 0 45px #ff8fcf66;animation:pulse 1.8s ease-in-out infinite}@keyframes pulse{50%{transform:scale(1.045);box-shadow:0 0 65px #99f0cf55}}h1{font-size:clamp(30px,5vw,54px);margin:0;letter-spacing:-.04em}.tag{color:var(--muted);font-size:16px;margin-top:5px}.notice{border:1px solid #574c72;background:#171523cc;border-radius:18px;padding:15px 17px;color:#ddd6e6;margin-bottom:22px}.grid{display:grid;grid-template-columns:310px 1fr;gap:18px}.panel{background:#191725dd;border:1px solid var(--line);border-radius:22px;padding:18px;box-shadow:0 12px 40px #0004}.panel h2{margin:0 0 12px;font-size:19px}.lantern-list{display:grid;gap:9px;max-height:450px;overflow:auto}.lantern{border:1px solid var(--line);background:var(--soft);padding:12px;border-radius:15px;cursor:pointer}.lantern.active{border-color:var(--mint);box-shadow:0 0 0 2px #99f0cf20}.small{font-size:12px;color:var(--muted)}button,.button{appearance:none;border:0;border-radius:13px;padding:11px 14px;font:inherit;font-weight:750;background:linear-gradient(135deg,var(--pink),var(--gold));color:#241525;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:7px}button.secondary{background:var(--soft);color:var(--text);border:1px solid var(--line)}button.mint{background:linear-gradient(135deg,var(--mint),#d6ffb6)}button:disabled{opacity:.5;cursor:not-allowed}input,textarea,select{width:100%;border:1px solid var(--line);background:#0f0e17;color:var(--text);border-radius:12px;padding:11px 12px;font:inherit}textarea{min-height:90px;resize:vertical}label{display:block;font-size:13px;color:var(--muted);margin:10px 0 6px}.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.row>*{flex:1}.stack{display:grid;gap:12px}.tabs{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:15px}.tab{background:var(--soft);color:var(--muted);border:1px solid var(--line);padding:9px 12px}.tab.active{color:#201827;background:var(--mint)}.view{display:none}.view.active{display:block}.drop{border:2px dashed #56506b;border-radius:18px;padding:28px;text-align:center;background:#12101c;transition:.2s}.drop.drag{border-color:var(--pink);background:#24172b}.drop strong{display:block;font-size:18px;margin-bottom:5px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin:14px 0}.stat{background:var(--soft);border-radius:14px;padding:12px}.stat b{font-size:24px;display:block}.good{color:var(--mint)}.dim{color:var(--muted)}.heart{font-size:55px;animation:pulse 1.1s ease-in-out infinite;display:inline-block}.timeline{display:grid;gap:8px}.item{padding:10px 12px;border-left:3px solid var(--pink);background:#12101c;border-radius:0 12px 12px 0}.empty{color:var(--muted);padding:18px;text-align:center;border:1px dashed var(--line);border-radius:14px}.toast{position:fixed;right:18px;bottom:18px;max-width:360px;background:#262139;border:1px solid #5c5574;padding:13px 15px;border-radius:14px;box-shadow:0 8px 28px #0008;display:none;z-index:20}.toast.show{display:block}.consent{display:flex;align-items:flex-start;gap:9px}.consent input{width:auto;margin-top:3px}.footer{text-align:center;color:var(--muted);font-size:12px;margin:24px 0 10px}@media(max-width:780px){.shell{padding:15px}.grid{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}.hero{align-items:flex-start}.orb{width:58px;height:58px;flex:0 0 auto}}
</style>
</head>
<body><div class="shell">
<div class="hero"><div class="orb" aria-hidden="true"></div><div><h1>HEARTLIGHT Home</h1><div class="tag">The Lantern Archive · preserve stories, rhythm, and family teaching with care.</div></div></div>
<div class="notice"><b>What this is:</b> a local-first memorial archive. A Lantern can preserve records and build a computational memorial profile. It does not claim a person has biologically returned, that a heartbeat contains a whole identity, or that consciousness after death has been proven.</div>
<div class="grid">
<aside class="panel"><h2>Your Lanterns</h2><div id="lanterns" class="lantern-list"></div><div style="height:12px"></div><button style="width:100%" onclick="showCreate()">＋ Create a Lantern</button></aside>
<main class="panel">
<div id="welcome"><h2>One little light is enough to begin.</h2><p class="dim">Create a Lantern, add the memories you choose, add a heartbeat recording if you have one, then teach the archive what mattered.</p></div>
<div id="workspace" style="display:none">
<div class="row"><div><h2 id="title" style="margin-bottom:2px"></h2><div id="projectId" class="small"></div></div><button class="secondary" onclick="downloadArchive()">⬇ Backup</button></div>
<div id="stats" class="stats"></div>
<div class="tabs"><button class="tab active" data-view="memories">Memories</button><button class="tab" data-view="heartbeat">Heartbeat</button><button class="tab" data-view="teach">Teach</button><button class="tab" data-view="build">Build</button></div>
<section class="view active" id="view-memories"><div id="drop" class="drop"><strong>Drop photos, videos, audio, or text here</strong><span class="dim">or choose files from your device</span><div style="height:12px"></div><input id="evidenceFiles" type="file" multiple hidden /><button class="secondary" onclick="document.getElementById('evidenceFiles').click()">Choose files</button></div><label>Where are these memories from?</label><input id="evidenceSource" placeholder="Family photo album, Dad's phone, Grandma's letters…" value="family archive"/><label>Optional note</label><input id="evidenceNotes" placeholder="Christmas 2019, favorite story, voice memo…"/><div id="uploadStatus" class="small" style="margin-top:10px"></div></section>
<section class="view" id="view-heartbeat"><div style="text-align:center"><div class="heart">🫀</div><h2>Add a heartbeat rhythm</h2><p class="dim">Use an uncompressed PCM WAV recording when possible. HEARTLIGHT extracts timing features and a reproducible rhythm digest; it is not a medical or biometric identity test.</p><input id="heartFile" type="file" accept="audio/wav,.wav"/><div style="height:10px"></div><button class="mint" onclick="uploadHeartbeat()">Analyze heartbeat</button><pre id="heartResult" class="small" style="white-space:pre-wrap;text-align:left"></pre></div></section>
<section class="view" id="view-teach"><h2>Teach the Lantern</h2><p class="dim">Family teaching is append-only and source-labeled. You can preserve different memories without pretending everyone remembers the same thing.</p><label>Who is teaching?</label><input id="teacher" placeholder="Mom, Dad, sister, friend…"/><label>Memory prompt</label><input id="prompt" placeholder="What did Sunday mornings feel like?"/><label>What should the archive remember?</label><textarea id="response" placeholder="Coffee, old music, everybody talking too loud…"></textarea><button onclick="teach()">Save this memory</button></section>
<section class="view" id="view-build"><h2>Build the Lantern profile</h2><p class="dim">This gathers the evidence manifest, text corpus, family teaching, and optional heartbeat signature into one grounded profile for future memorial experiences.</p><button class="mint" onclick="buildLantern()">✨ Build Lantern</button><div id="buildResult" style="margin-top:14px"></div></section>
</div></main>
</div>
<div class="footer">Local-first by default · no cloud account required · family media remains family media.</div>
</div>
<div id="createModal" style="display:none;position:fixed;inset:0;background:#000b;z-index:10;padding:20px"><div class="panel" style="max-width:520px;margin:8vh auto"><h2>Create a Lantern</h2><label>Who or what is this Lantern remembering?</label><input id="newName" placeholder="Grandma Rose's Lantern"/><div class="consent"><input id="consent" type="checkbox"/><label for="consent" style="margin:0">I understand HEARTLIGHT creates a memorial archive/simulation from supplied records and teaching. It does not prove resurrection or identity transfer, and I have permission to use the records I add.</label></div><div class="row" style="margin-top:16px"><button class="secondary" onclick="hideCreate()">Cancel</button><button onclick="createLantern()">Create</button></div></div></div>
<div id="toast" class="toast"></div>
<script>
let current=null;
const $=id=>document.getElementById(id);
function toast(msg,good=true){const t=$('toast');t.textContent=msg;t.style.borderColor=good?'#99f0cf':'#ff9aa8';t.classList.add('show');setTimeout(()=>t.classList.remove('show'),3200)}
async function api(url,opts={}){const r=await fetch(url,opts);if(!r.ok){let m='Something went wrong';try{const j=await r.json();m=j.detail||m}catch{}throw new Error(m)}const ct=r.headers.get('content-type')||'';return ct.includes('json')?r.json():r}
function showCreate(){$('createModal').style.display='block';$('newName').focus()}function hideCreate(){$('createModal').style.display='none'}
async function createLantern(){const name=$('newName').value.trim();if(!name)return toast('Give the Lantern a name.',false);if(!$('consent').checked)return toast('Please read and accept the archive disclosure.',false);try{const j=await api('/api/projects',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({display_name:name})});hideCreate();$('newName').value='';$('consent').checked=false;await loadLanterns(j.project)}catch(e){toast(e.message,false)}}
async function loadLanterns(select=null){const list=await api('/api/projects');$('lanterns').innerHTML=list.length?'':'<div class="empty">No Lanterns yet.</div>';for(const x of list){const d=document.createElement('div');d.className='lantern'+((select||current)===x.project?' active':'');d.innerHTML=`<b>${escapeHtml(x.display_name)}</b><div class="small">${x.artifacts} memories · ${x.lessons} teachings</div>`;d.onclick=()=>selectLantern(x.project);$('lanterns').appendChild(d)}if(select)await selectLantern(select);else if(current)await selectLantern(current)}
async function selectLantern(id){current=id;const s=await api(`/api/projects/${id}/status`);$('welcome').style.display='none';$('workspace').style.display='block';$('title').textContent=s.display_name;$('projectId').textContent='Lantern '+s.project_id.slice(0,8);$('stats').innerHTML=`<div class="stat"><b>${s.artifacts}</b><span class="small">memories</span></div><div class="stat"><b>${s.lessons}</b><span class="small">teachings</span></div><div class="stat"><b class="${s.heartbeat_signature?'good':'dim'}">${s.heartbeat_signature?'✓':'—'}</b><span class="small">heartbeat</span></div><div class="stat"><b class="${s.profile_built?'good':'dim'}">${s.profile_built?'✓':'—'}</b><span class="small">built</span></div>`;await loadLanternsNoSelect()}
async function loadLanternsNoSelect(){const list=await api('/api/projects');const nodes=[...$('lanterns').children];nodes.forEach(n=>n.classList.remove('active'));list.forEach((x,i)=>{if(x.project===current&&nodes[i])nodes[i].classList.add('active')})}
function escapeHtml(s){return s.replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
async function uploadEvidence(files){if(!current||!files.length)return;const fd=new FormData();for(const f of files)fd.append('files',f);fd.append('source',$('evidenceSource').value.trim()||'family archive');fd.append('notes',$('evidenceNotes').value.trim());$('uploadStatus').textContent=`Adding ${files.length} file(s)…`;try{const j=await api(`/api/projects/${current}/evidence`,{method:'POST',body:fd});$('uploadStatus').textContent=`Added ${j.added} memory file(s).`;toast('Memories safely added.');await selectLantern(current)}catch(e){$('uploadStatus').textContent='';toast(e.message,false)}}
$('evidenceFiles').addEventListener('change',e=>uploadEvidence([...e.target.files]));const drop=$('drop');['dragenter','dragover'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('drag')}));['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('drag')}));drop.addEventListener('drop',e=>uploadEvidence([...e.dataTransfer.files]));
async function uploadHeartbeat(){const f=$('heartFile').files[0];if(!current||!f)return toast('Choose a WAV heartbeat recording first.',false);const fd=new FormData();fd.append('file',f);try{const j=await api(`/api/projects/${current}/heartbeat`,{method:'POST',body:fd});$('heartResult').textContent=`Estimated BPM: ${j.estimated_bpm??'not enough distinct beats'}\nDetected beats: ${j.beat_times_seconds.length}\nRhythm digest: ${j.rhythm_digest.slice(0,20)}…`;toast('Heartbeat rhythm added.');await selectLantern(current)}catch(e){toast(e.message,false)}}
async function teach(){if(!current)return;const payload={teacher:$('teacher').value.trim(),prompt:$('prompt').value.trim(),response:$('response').value.trim()};if(!payload.teacher||!payload.prompt||!payload.response)return toast('Fill in the teacher, prompt, and memory.',false);try{await api(`/api/projects/${current}/lessons`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(payload)});$('prompt').value='';$('response').value='';toast('Memory teaching saved.');await selectLantern(current)}catch(e){toast(e.message,false)}}
async function buildLantern(){if(!current)return;try{const j=await api(`/api/projects/${current}/build`,{method:'POST'});$('buildResult').innerHTML=`<div class="item"><b>Lantern built.</b><div class="small">${j.evidence.length} evidence records · ${j.family_teaching.length} family teachings · ${j.heartbeat_signature?'heartbeat connected':'no heartbeat required'}</div></div>`;toast('Lantern profile built.');await selectLantern(current)}catch(e){toast(e.message,false)}}
function downloadArchive(){if(current)location.href=`/api/projects/${current}/export`}
document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>{document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));b.classList.add('active');$('view-'+b.dataset.view).classList.add('active')});
if('serviceWorker'in navigator)navigator.serviceWorker.register('/sw.js').catch(()=>{});loadLanterns().catch(e=>toast(e.message,false));
</script></body></html>'''

PWA_MANIFEST = {
    "name": "HEARTLIGHT Home",
    "short_name": "HEARTLIGHT",
    "description": "Local-first family memorial archive",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0f0e17",
    "theme_color": "#171523",
    "icons": [],
}

SERVICE_WORKER = """const CACHE='heartlight-home-v1';self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['/','/manifest.webmanifest']))));self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(u.pathname.startsWith('/api/'))return;e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));});"""


def create_app():
    try:
        from fastapi import FastAPI, File, Form, HTTPException, UploadFile
        from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
        from pydantic import BaseModel, Field
        from starlette.background import BackgroundTask
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install HEARTLIGHT Home support with: pip install -e '.[home]'") from exc

    app = FastAPI(title=APP_NAME, version=APP_VERSION, docs_url=None, redoc_url=None)

    class CreateLantern(BaseModel):
        display_name: str = Field(min_length=1, max_length=256)

    class Lesson(BaseModel):
        prompt: str = Field(min_length=1, max_length=8000)
        response: str = Field(min_length=1, max_length=32000)
        teacher: str = Field(min_length=1, max_length=256)

    @app.get("/", response_class=HTMLResponse)
    def home_page():
        return HOME_HTML

    @app.get("/manifest.webmanifest")
    def manifest():
        return JSONResponse(PWA_MANIFEST, media_type="application/manifest+json")

    @app.get("/sw.js", response_class=PlainTextResponse)
    def service_worker():
        return PlainTextResponse(SERVICE_WORKER, media_type="application/javascript")

    @app.get("/healthz")
    def healthz():
        return {"ok": True, "service": "heartlight-home", "version": APP_VERSION}

    @app.get("/api/projects")
    def projects():
        return _list_projects()

    @app.post("/api/projects", status_code=201)
    def create_project(body: CreateLantern):
        try:
            slug = _slugify(body.display_name)
            vault = init_project(_project_path(slug), body.display_name.strip())
            return {"project": slug, "manifest": vault.read_manifest()}
        except (ValueError, FileExistsError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/api/projects/{project}/status")
    def project_status(project: str):
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
    ):
        if not files:
            raise HTTPException(status_code=400, detail="choose at least one file")
        added = 0
        records: list[dict] = []
        for upload in files:
            filename = Path(upload.filename or "memory.bin").name
            suffix = Path(filename).suffix
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp:
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
                # Preserve the human-friendly original filename in the manifest record.
                vault = open_vault(_project_path(project)).require()
                manifest_data = vault.read_manifest()
                for item in manifest_data.get("artifacts", []):
                    if item.get("artifact_id") == record.artifact_id:
                        item["original_name"] = filename
                atomic_write_json(vault.manifest, manifest_data)
                records.append(record.to_dict() | {"original_name": filename})
                added += 1
            finally:
                temp_path.unlink(missing_ok=True)
        return {"added": added, "records": records}

    @app.post("/api/projects/{project}/heartbeat", status_code=201)
    async def upload_heartbeat(project: str, file: Annotated[UploadFile, File()]):
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
    def save_lesson(project: str, body: Lesson):
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
    def build(project: str):
        try:
            return build_profile(_project_path(project))
        except (ValueError, FileNotFoundError) as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/projects/{project}/export")
    def export(project: str):
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


def _find_port(preferred: int = 8787) -> int:
    for port in range(preferred, preferred + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError("Could not find an available local port for HEARTLIGHT Home")


def main() -> int:
    try:
        import uvicorn
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install HEARTLIGHT Home support with: pip install -e '.[home]'") from exc
    _home_root()
    port = _find_port()
    url = f"http://127.0.0.1:{port}/"
    threading.Timer(0.9, lambda: webbrowser.open(url)).start()
    uvicorn.run(create_app(), host="127.0.0.1", port=port, log_level="warning", access_log=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
