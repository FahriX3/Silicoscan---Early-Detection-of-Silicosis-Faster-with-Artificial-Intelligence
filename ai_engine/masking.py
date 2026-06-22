"""
masking.py — U-Net Lung Masking Pipeline
=========================================
Segmentasi paru-paru menggunakan U-Net (ResNet34 backbone).
Area luar paru-paru dijadikan hitam → fokus analisis hanya di area paru.
"""

import cv2
import numpy as np
import onnxruntime as ort


# ==================== MASKING ENGINE ====================

class LungMaskingEngine:
    """Engine untuk segmentasi paru-paru menggunakan U-Net."""

    def __init__(self, model_path, device, img_size=256):
        self.device = device
        self.img_size = img_size
        self.ort_session = self._load_model(model_path)
        print(f"  [Masking] U-Net ONNX loaded")

    def _load_model(self, model_path):
        providers = ['CPUExecutionProvider']
        session = ort.InferenceSession(str(model_path), providers=providers)
        return session

    def preprocess(self, image):
        """Pre-process: Grayscale → Resize → CLAHE → Normalize → Tensor."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        resized = cv2.resize(gray, (self.img_size, self.img_size), interpolation=cv2.INTER_LINEAR)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(resized)
        normalized = enhanced.astype(np.float32) / 255.0
        # Expand dims untuk jadi [1, 1, H, W]
        input_data = np.expand_dims(np.expand_dims(normalized, axis=0), axis=0)
        return input_data

    def postprocess(self, raw_mask, original_size, threshold=0.5, min_area=500):
        """Post-process: Threshold → Morphology → Connected Components → Resize."""
        binary = (raw_mask > threshold).astype(np.uint8) * 255

        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_open, iterations=2)

        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close, iterations=2)

        # Keep top 2 largest connected components (kanan + kiri paru)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(closed)
        if num_labels > 1:
            areas = stats[1:, cv2.CC_STAT_AREA]
            label_indices = np.arange(1, num_labels)
            valid = areas >= min_area
            valid_indices = label_indices[valid]
            valid_areas = areas[valid]

            if len(valid_indices) > 0:
                top = valid_indices[np.argsort(valid_areas)[::-1][:2]]
                cleaned = np.zeros_like(closed)
                for lid in top:
                    cleaned[labels == lid] = 255
            else:
                cleaned = np.zeros_like(closed)
        else:
            cleaned = closed

        return cv2.resize(cleaned, original_size, interpolation=cv2.INTER_NEAREST)

    def mask(self, image):
        """
        Main masking function.

        Args:
            image: numpy array BGR (H, W, 3) atau grayscale (H, W)

        Returns:
            dict: {
                'masked_image': gambar dengan area luar paru hitam,
                'mask': binary mask (0/255),
                'mask_ratio': rasio area paru terhadap total
            }
        """
        orig_h, orig_w = image.shape[:2]

        # Predict
        input_data = self.preprocess(image)
        ort_inputs = {self.ort_session.get_inputs()[0].name: input_data}
        ort_outs = self.ort_session.run(None, ort_inputs)
        
        output = ort_outs[0]
        prob = 1 / (1 + np.exp(-output))  # Sigmoid

        raw_mask = np.squeeze(prob)

        # Post-process
        clean_mask = self.postprocess(raw_mask, (orig_w, orig_h))

        # Apply mask (bitwise AND)
        if len(image.shape) == 3:
            mask_3ch = cv2.merge([clean_mask, clean_mask, clean_mask])
            masked = cv2.bitwise_and(image, mask_3ch)
        else:
            masked = cv2.bitwise_and(image, image, mask=clean_mask)

        mask_ratio = np.count_nonzero(clean_mask) / (orig_h * orig_w)

        return {
            "masked_image": masked,
            "mask": clean_mask,
            "mask_ratio": mask_ratio,
        }
