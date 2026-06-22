"""
pipeline.py — AI Pipeline Orchestrator
========================================
Mengorkestrasi 3 model AI secara berurutan:
  1. U-Net Masking  → Segmentasi paru
  2. Swin Classifier → Klasifikasi (Normal/Abnormal)
  3. YOLO Detector   → Deteksi lokasi lesi (hanya jika abnormal)
"""

import time
import cv2
import numpy as np
import base64
from io import BytesIO

from .masking import LungMaskingEngine
from .detector import LungDetectorEngine


def numpy_to_base64(image, ext=".jpg", quality=90):
    """Convert numpy image ke base64 string untuk frontend."""
    if ext == ".png":
        _, buffer = cv2.imencode(".png", image)
    else:
        _, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return base64.b64encode(buffer).decode("utf-8")


class ScreeningPipeline:
    """
    Pipeline utama skrining paru-paru.
    Load semua model sekali di awal, kemudian bisa dipanggil berulang.
    """

    def __init__(self, config):
        """
        Args:
            config: module config.py yang berisi semua settings
        """
        self.config = config
        self.device = config.DEVICE
        self._loaded = False

        self.masking_engine = None
        self.detector_engine = None
        self.detector_full_engine = None

    def load_models(self):
        """Load semua model ke memory. Panggil sekali saat startup."""
        print("=" * 60)
        print(f"  {self.config.APP_NAME} — Loading AI Models")
        print("=" * 60)
        print(f"  Device: {self.device}")

        start = time.time()

        # 1. U-Net Masking
        self.masking_engine = LungMaskingEngine(
            model_path=self.config.MASKING_MODEL_PATH,
            device=self.device,
            img_size=self.config.MASKING_IMG_SIZE,
        )

        # 2. YOLO Detector Biasa
        self.detector_engine = LungDetectorEngine(
            model_path=self.config.DETECTOR_MODEL_PATH,
            device=self.device,
            class_config=self.config.DETECTOR_CLASSES,
            conf_threshold=self.config.DETECTOR_CONF_THRESHOLD,
        )

        # 3. YOLO Detector Full
        self.detector_full_engine = LungDetectorEngine(
            model_path=self.config.DETECTOR_FULL_MODEL_PATH,
            device=self.device,
            class_config=self.config.DETECTOR_FULL_CLASSES,
            conf_threshold=self.config.DETECTOR_CONF_THRESHOLD,
        )

        elapsed = time.time() - start
        print(f"\n  All models loaded in {elapsed:.1f}s")
        print("=" * 60)

        self._loaded = True

    def analyze(self, image_bytes, model_type="biasa"):
        """
        Analisis lengkap dari bytes gambar.

        Args:
            image_bytes: bytes dari file upload
            model_type: string ('biasa' atau 'full') untuk memilih model deteksi

        Returns:
            dict: Hasil analisis lengkap
        """
        if not self._loaded:
            raise RuntimeError("Models belum di-load! Panggil load_models() dulu.")

        total_start = time.time()
        steps = []

        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        raw_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if raw_image is None:
            raise ValueError("Gagal membaca gambar. Pastikan format JPG/PNG yang valid.")

        orig_h, orig_w = raw_image.shape[:2]

        # ============================================
        # TAHAP 0: U-Net Masking
        # ============================================
        t0 = time.time()
        mask_result = self.masking_engine.mask(raw_image)
        t0_elapsed = time.time() - t0

        masked_image = mask_result["masked_image"]
        mask_ratio = mask_result["mask_ratio"]

        steps.append({
            "step": 0,
            "name": "Segmentasi Paru (U-Net)",
            "status": "success" if mask_ratio > 0.05 else "warning",
            "time_ms": int(t0_elapsed * 1000),
            "detail": f"Area paru terdeteksi: {mask_ratio:.1%}",
        })

        if mask_ratio < 0.05:
            # Mask terlalu kecil, mungkin bukan foto rontgen paru
            return {
                "success": False,
                "error": "Area paru-paru tidak terdeteksi. Pastikan gambar adalah foto rontgen dada (chest X-ray) yang valid.",
                "image_size": f"{orig_w}x{orig_h}",
                "steps": steps,
                "total_time_ms": int((time.time() - total_start) * 1000),
            }

        # ============================================
        # TAHAP 1: YOLO Detection
        # ============================================
        detector = self.detector_full_engine if model_type == "full" else self.detector_engine
        
        t1 = time.time()
        detection_result = detector.detect(masked_image, raw_image)
        t1_elapsed = time.time() - t1

        steps.append({
            "step": 1,
            "name": f"Deteksi Lokasi Lesi (YOLO {model_type.capitalize()})",
            "status": "success",
            "time_ms": int(t1_elapsed * 1000),
            "detail": f"{detection_result['num_detections']} area terdeteksi",
        })

        annotated_b64 = numpy_to_base64(detection_result["annotated_image"])
        is_normal = detection_result["num_detections"] == 0

        # ============================================
        # Build response
        # ============================================
        total_elapsed = time.time() - total_start

        # Encode images untuk frontend
        original_b64 = numpy_to_base64(raw_image)
        masked_b64 = numpy_to_base64(masked_image)

        result = {
            "success": True,
            "image_size": f"{orig_w}x{orig_h}",
            "total_time_ms": int(total_elapsed * 1000),
            "steps": steps,

            # Masking
            "mask_ratio": mask_ratio,
            "is_normal": is_normal,

            # Deteksi
            "detection": {
                "performed": True,
                "num_detections": detection_result["num_detections"],
                "detections": detection_result["detections"],
            },

            # Images (base64)
            "images": {
                "original": original_b64,
                "masked": masked_b64,
                "annotated": annotated_b64,
            },
        }

        return result

    def save_annotated(self, image_bytes, output_path):
        """
        Simpan gambar annotated ke file.
        Berguna untuk download hasil.
        """
        result = self.analyze(image_bytes)
        if result["success"] and result["images"]["annotated"]:
            img_data = base64.b64decode(result["images"]["annotated"])
            with open(output_path, "wb") as f:
                f.write(img_data)
            return True
        return False
