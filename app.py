"""
app.py — Silicoscan FastAPI Application
==========================================
Sistem Skrining Paru-Paru Berbasis AI untuk Deteksi Dini Silikosis.

Usage:
    python app.py
    # atau
    uvicorn app:app --host 0.0.0.0 --port 8000
"""

import os
import uuid
import time
import base64
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import config
from ai_engine.pipeline import ScreeningPipeline

# ==================== APP INIT ====================

app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description=config.APP_DESCRIPTION,
)

# CORS (untuk development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files & templates
STATIC_DIR = Path(__file__).parent / "static"
TEMPLATES_DIR = Path(__file__).parent / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ==================== AI PIPELINE ====================

pipeline = ScreeningPipeline(config)


@app.on_event("startup")
async def startup_event():
    """Load semua model AI saat server start."""
    pipeline.load_models()
    print(f"\n🚀 {config.APP_NAME} v{config.APP_VERSION} ready!")
    print(f"   Open http://localhost:{config.APP_PORT} in your browser\n")


# ==================== ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Halaman utama (landing page)."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": config.APP_NAME,
        "app_version": config.APP_VERSION,
        "app_description": config.APP_DESCRIPTION,
    })


@app.get("/screening", response_class=HTMLResponse)
async def screening(request: Request):
    """Halaman skrining AI."""
    return templates.TemplateResponse("screening.html", {
        "request": request,
        "app_name": config.APP_NAME,
        "app_version": config.APP_VERSION,
        "app_description": config.APP_DESCRIPTION,
    })


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...), model_type: str = Form("biasa")):
    """
    Upload & analisis gambar rontgen paru.
    Returns JSON dengan hasil deteksi.
    """
    # Validasi file
    if not file.filename:
        raise HTTPException(400, "Tidak ada file yang di-upload")

    ext = Path(file.filename).suffix.lower()
    if ext not in config.ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Format file tidak didukung: {ext}. Gunakan JPG/PNG.")

    # Baca file
    contents = await file.read()
    if len(contents) > config.MAX_UPLOAD_SIZE:
        raise HTTPException(400, f"File terlalu besar (max {config.MAX_UPLOAD_SIZE // 1024 // 1024}MB)")

    if len(contents) == 0:
        raise HTTPException(400, "File kosong")

    # Analisis
    try:
        result = pipeline.analyze(contents, model_type)
    except Exception as e:
        raise HTTPException(500, f"Error saat analisis: {str(e)}")

    # Simpan annotated image jika ada (untuk download nanti)
    if result["success"] and result["images"].get("annotated"):
        result_id = str(uuid.uuid4())[:8]
        annotated_path = config.RESULTS_DIR / f"{result_id}_annotated.jpg"
        img_data = base64.b64decode(result["images"]["annotated"])
        with open(annotated_path, "wb") as f:
            f.write(img_data)
        result["download_id"] = result_id

    return JSONResponse(result)


@app.get("/api/download/{result_id}")
async def download_result(result_id: str):
    """Download gambar hasil annotated."""
    file_path = config.RESULTS_DIR / f"{result_id}_annotated.jpg"
    if not file_path.exists():
        raise HTTPException(404, "File tidak ditemukan")
    return FileResponse(
        str(file_path),
        media_type="image/jpeg",
        filename=f"silicoscan_result_{result_id}.jpg",
    )


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": config.APP_NAME,
        "version": config.APP_VERSION,
        "device": str(config.DEVICE),
        "models_loaded": pipeline._loaded,
    }


# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=False,
    )
