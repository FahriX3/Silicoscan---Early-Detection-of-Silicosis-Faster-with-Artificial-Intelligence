"""
detector.py — YOLO Detection Pipeline
=======================================
Deteksi lokasi abnormalitas pada paru menggunakan YOLO11s.

Kelas deteksi:
  0: Silicosis_Nodular      — Nodul + Reticulonodular opacity
  1: Silicosis_Advanced_Fibrotic — Fibrosis + Cavity + Hilar abnormality
  2: Other_Lung_Abnormality  — Consolidation, Emphysema, Pleural, GGO, dll
"""

import cv2
import numpy as np
import tempfile
import os
from pathlib import Path


class LungDetectorEngine:
    """Engine untuk deteksi abnormalitas paru menggunakan YOLO11."""

    def __init__(self, model_path, device, class_config, conf_threshold=0.6):
        self.device = device
        self.class_config = class_config
        self.conf_threshold = conf_threshold

        # Import ultralytics di sini supaya lazy load
        from ultralytics import YOLO
        self.model = YOLO(str(model_path))
        print(f"  [Detector] YOLO11s loaded (conf={conf_threshold})")

    def detect(self, masked_image, raw_image, conf_threshold=None):
        """
        Deteksi abnormalitas pada masked image, gambar bbox di raw image.

        Args:
            masked_image: numpy array BGR — image yang sudah di-mask (input YOLO)
            raw_image: numpy array BGR — image asli (untuk visualisasi bbox)
            conf_threshold: override confidence threshold

        Returns:
            dict: {
                'annotated_image': raw image dengan bounding boxes,
                'detections': list of detection dicts,
                'num_detections': int,
            }
        """
        conf = conf_threshold or self.conf_threshold

        # YOLO butuh file path, simpan sementara
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "masked_input.jpg")
        cv2.imwrite(temp_path, masked_image, [cv2.IMWRITE_JPEG_QUALITY, 95])

        try:
            results = self.model.predict(
                source=temp_path,
                conf=conf,
                imgsz=640,
                device=str(self.device),  # EXPLISIT DEVICE (cpu/cuda)
                verbose=False,
            )
        finally:
            # Cleanup temp
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)

        # Parse results
        boxes = results[0].boxes if len(results) > 0 else None
        annotated, detections = self._draw_on_original(raw_image, boxes, conf)

        return {
            "annotated_image": annotated,
            "detections": detections,
            "num_detections": len(detections),
        }

    def _draw_on_original(self, original_image, boxes, conf_threshold):
        """Gambar bounding box deteksi di atas gambar original (raw)."""
        annotated = original_image.copy()
        img_h, img_w = annotated.shape[:2]
        detection_info = []

        if boxes is None or len(boxes) == 0:
            return annotated, detection_info

        xyxy = boxes.xyxy.cpu().numpy()
        confs = boxes.conf.cpu().numpy()
        classes = boxes.cls.cpu().numpy().astype(int)

        for i in range(len(xyxy)):
            conf = confs[i]
            if conf < conf_threshold:
                continue

            cls_id = classes[i]
            x1, y1, x2, y2 = xyxy[i].astype(int)

            # Clamp
            x1 = max(0, min(x1, img_w - 1))
            y1 = max(0, min(y1, img_h - 1))
            x2 = max(0, min(x2, img_w - 1))
            y2 = max(0, min(y2, img_h - 1))

            cls_info = self.class_config.get(cls_id, {
                "id": f"class_{cls_id}",
                "label": f"Class {cls_id}",
                "color_bgr": (255, 255, 255),
            })

            color = cls_info["color_bgr"]
            label_text = cls_info["label"]

            # Draw rectangle
            thickness = max(2, int(min(img_w, img_h) / 300))
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)

            # Draw label
            label = f"{label_text} {conf:.0%}"
            font_scale = max(0.5, min(img_w, img_h) / 1500)
            font_thickness = max(1, int(font_scale * 2))
            (tw, th), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
            )

            label_y1 = max(0, y1 - th - baseline - 6)
            cv2.rectangle(annotated, (x1, label_y1), (x1 + tw + 4, y1), color, -1)
            cv2.putText(
                annotated, label,
                (x1 + 2, y1 - baseline - 2),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                (0, 0, 0), font_thickness, cv2.LINE_AA,
            )

            detection_info.append({
                "class_id": int(cls_id),
                "class_name": cls_info["id"],
                "class_label": label_text,
                "confidence": float(conf),
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "color": cls_info.get("color", "#FFFFFF"),
            })

        return annotated, detection_info
