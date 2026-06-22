"""
config.py — Konfigurasi Silicoscan
====================================
Semua settings aplikasi ada di sini.
"""

import os
import torch
from pathlib import Path

# ==================== PATHS ====================
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent  # Medis Final Model/

# Model weights
MODELS_DIR = BASE_DIR / "models"

MASKING_MODEL_PATH = MODELS_DIR / "unet_masking_fp32.onnx"
DETECTOR_MODEL_PATH = MODELS_DIR / "yolo_deteksi_biasa_fp16.onnx"
DETECTOR_FULL_MODEL_PATH = MODELS_DIR / "yolo_deteksi_full_fp16.onnx"

# Upload & output directories
UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# ==================== DEVICE ====================
# Memaksa penggunaan CPU karena GPU NVIDIA seri 5000 (Blackwell)
# belum disupport penuh oleh versi PyTorch stabil saat ini.
# Inference dengan CPU tetap sangat cepat (~2 detik).
DEVICE = torch.device("cpu")

# ==================== MODEL SETTINGS ====================

# U-Net Masking
MASKING_IMG_SIZE = 256
MASKING_THRESHOLD = 0.5
MASKING_MIN_AREA = 500

# Removed Swin Classifier

# YOLO Detector Biasa
DETECTOR_CONF_THRESHOLD = 0.6
DETECTOR_IMG_SIZE = 640

DETECTOR_CLASSES = {
    0: {
        "id": "nodular",
        "label": "Silikosis Nodular",
        "description": "Nodul/Reticulonodular opacity — tanda awal silikosis",
        "color": "#FFFF00",  # Yellow
        "color_bgr": (0, 255, 255),
    },
    1: {
        "id": "fibrotic",
        "label": "Silikosis Lanjut (Fibrotik)",
        "description": "Fibrosis/Kavitas/Abnormalitas hilus — silikosis stadium lanjut",
        "color": "#FF4444",  # Red
        "color_bgr": (0, 0, 255),
    },
    2: {
        "id": "other",
        "label": "Abnormalitas Paru Lainnya",
        "description": "Konsolidasi/Emfisema/Kelainan pleura/GGO/Bronkiektasis",
        "color": "#FFA500",  # Orange
        "color_bgr": (255, 165, 0),
    },
}

DETECTOR_FULL_CLASSES = {
    0: {"id": "nodules", "label": "Nodules", "description": "Nodules", "color": "#FFFF00", "color_bgr": (0, 255, 255)},
    1: {"id": "reticulonodular", "label": "Reticulonodular Opacity", "description": "Reticulonodular Opacity", "color": "#FFA500", "color_bgr": (0, 165, 255)},
    2: {"id": "consolidation", "label": "Consolidation", "description": "Consolidation", "color": "#FF4500", "color_bgr": (0, 69, 255)},
    3: {"id": "fibrosis", "label": "Fibrosis", "description": "Fibrosis", "color": "#FF0000", "color_bgr": (0, 0, 255)},
    4: {"id": "hilar", "label": "Hilar Abnormality", "description": "Hilar Abnormality", "color": "#DC143C", "color_bgr": (60, 20, 220)},
    5: {"id": "cavity", "label": "Cavity", "description": "Cavity", "color": "#8B0000", "color_bgr": (0, 0, 139)},
    6: {"id": "pleural", "label": "Pleural Abnormality", "description": "Pleural Abnormality", "color": "#800080", "color_bgr": (128, 0, 128)},
    7: {"id": "ggo", "label": "Ground Glass Opacity", "description": "Ground Glass Opacity", "color": "#4169E1", "color_bgr": (225, 105, 65)},
    8: {"id": "emphysema", "label": "Emphysema", "description": "Emphysema", "color": "#00BFFF", "color_bgr": (255, 191, 0)},
    9: {"id": "bronchiectasis", "label": "Bronchiectasis", "description": "Bronchiectasis", "color": "#00CED1", "color_bgr": (209, 206, 0)},
    10: {"id": "other", "label": "Other", "description": "Other Abnormalities", "color": "#008000", "color_bgr": (0, 128, 0)},
}

# ==================== APP SETTINGS ====================
APP_NAME = "Silicoscan"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistem Skrining Paru-Paru Berbasis AI untuk Deteksi Dini Silikosis"
APP_HOST = "0.0.0.0"
APP_PORT = 8000

# Max upload size (30MB)
MAX_UPLOAD_SIZE = 30 * 1024 * 1024
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
