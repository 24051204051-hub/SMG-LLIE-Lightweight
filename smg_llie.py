import cv2
import numpy as np
import matplotlib.pyplot as plt


class SMG_LLIE_Enhancer:
    """
    SMG-LLIE Enhancer (Lightweight Version)
    
    NOTE:
    Class ini adalah inti dari sistem.
    Berisi pipeline peningkatan citra low-light berbasis:
    - Struktur (edge & detail)
    - Appearance (perbaikan visual)
    - Frekuensi (detail halus)
    - Gamma adaptif (kecerahan akhir)
    """

    def __init__(self, gamma_base=1.5, structure_weight=0.8):
        # NOTE:
        # gamma_base → kontrol dasar kecerahan
        # structure_weight → seberapa kuat edge mempengaruhi hasil akhir
        self.gamma_base = gamma_base
        self.structure_weight = structure_weight

    def structure_modeling(self, img):
        """
        NOTE:
        Mengambil informasi STRUKTUR dari gambar:
        - Sobel → mendeteksi gradien (arah tepi)
        - Canny → mendeteksi edge tajam
        
        Tujuan:
        Supaya detail penting tidak hilang saat gambar diperjelas
        """
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_xy = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=3)

        magnitude = np.sqrt(sobel_x**2 + sobel_y**2 + sobel_xy**2)

        edges = cv2.Canny(gray, 50, 150)

        structure = cv2.normalize(magnitude + edges, None, 0, 255, cv2.NORM_MINMAX)

        print("[INFO] Structure Modeling done")
        return structure.astype(np.uint8)

    def appearance_modeling(self, img):
        """
        NOTE:
        Simulasi enhancement seperti U-Net (tanpa deep learning):
        - Blur → ambil informasi global
        - AddWeighted → tingkatkan kontras
        
        Tujuan:
        Membuat gambar terlihat lebih jelas tanpa kehilangan warna asli
        """
        blur1 = cv2.GaussianBlur(img, (5,5), 0)
        blur2 = cv2.GaussianBlur(blur1, (9,9), 0)

        enhanced = cv2.addWeighted(img, 1.5, blur2, -0.5, 0)

        print("[INFO] Appearance Modeling done")
        return np.clip(enhanced, 0, 255).astype(np.uint8)

    def structure_guided_enhancement(self, img, structure):
        """
        NOTE:
        Menggabungkan struktur ke dalam gambar:
        - Area dengan edge → diperkuat
        - Area flat → tidak terlalu diubah
        
        Tujuan:
        Detail tetap tajam setelah enhancement
        """
        structure_norm = structure / 255.0
        structure_norm = np.expand_dims(structure_norm, axis=2)

        enhanced = img * (1 + self.structure_weight * structure_norm)

        print("[INFO] Structure Guided Enhancement done")
        return np.clip(enhanced, 0, 255).astype(np.uint8)

    def frequency_refinement(self, img):
        """
        NOTE:
        Domain frekuensi (FFT):
        - Meningkatkan detail halus (high frequency)
        
        Tujuan:
        Menghindari hasil blur setelah enhancement
        """
        img_float = np.float32(img)

        fft = np.fft.fft2(img_float, axes=(0, 1))
        fft_shift = np.fft.fftshift(fft)

        magnitude = np.log(np.abs(fft_shift) + 1)
        boost = magnitude / np.max(magnitude)

        enhanced = img_float + boost * 30

        print("[INFO] Frequency Refinement done")
        return np.clip(enhanced, 0, 255).astype(np.uint8)

    def adaptive_gamma(self, img):
        """
        NOTE:
        Gamma disesuaikan otomatis:
        - Gambar gelap → gamma diperbesar
        - Gambar terang → gamma dikurangi
        
        Tujuan:
        Hasil akhir tidak overexposed / underexposed
        """
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mean_intensity = np.mean(gray)

        gamma = self.gamma_base + (128 - mean_intensity) / 128

        inv_gamma = 1.0 / gamma
        table = np.array([
            (i / 255.0) ** inv_gamma * 255
            for i in np.arange(256)
        ]).astype("uint8")

        print(f"[INFO] Gamma: {gamma:.2f}")
        return cv2.LUT(img, table)

    def enhance(self, image_path, visualize=False):
        """
        NOTE:
        Pipeline utama:
        1. Structure Modeling
        2. Appearance Modeling
        3. Structure Guided Enhancement
        4. Frequency Refinement
        5. Adaptive Gamma
        """
        img = cv2.imread(image_path)

        if img is None:
            raise ValueError(f"Image not found: {image_path}")

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        print(f"\n[PROCESSING] {image_path}")

        structure = self.structure_modeling(img)
        appearance = self.appearance_modeling(img)
        guided = self.structure_guided_enhancement(appearance, structure)
        freq = self.frequency_refinement(guided)
        final = self.adaptive_gamma(freq)

        import os

        filename = os.path.basename(image_path).split('.')[0]

        folder = f"data/output/{filename}"
        os.makedirs(folder, exist_ok=True)

        cv2.imwrite(f"{folder}/1_structure.jpg", structure)
        cv2.imwrite(f"{folder}/2_appearance.jpg", cv2.cvtColor(appearance, cv2.COLOR_RGB2BGR))
        cv2.imwrite(f"{folder}/3_guided.jpg", cv2.cvtColor(guided, cv2.COLOR_RGB2BGR))
        cv2.imwrite(f"{folder}/4_frequency.jpg", cv2.cvtColor(freq, cv2.COLOR_RGB2BGR))
        cv2.imwrite(f"{folder}/5_final.jpg", cv2.cvtColor(final, cv2.COLOR_RGB2BGR))

        print(f"✅ Disimpan di folder: {folder}")

        if visualize:
            self.visualize(img, structure, appearance, guided, freq, final)

        return final