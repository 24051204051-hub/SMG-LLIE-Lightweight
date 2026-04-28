# SMG-LLIE: Structure Modeling Guided Low-Light Image Enhancement

## 1. Latar Belakang
Citra dengan kondisi pencahayaan rendah (low-light image) sering mengalami:
- Noise tinggi
- Kontras rendah
- Detail tidak terlihat

Metode SMG-LLIE digunakan untuk meningkatkan kualitas citra dengan pendekatan:
- Struktur (edge-aware)
- Appearance (visual enhancement)
- Refinement berbasis frekuensi

---

## 2. Tujuan Sistem
Sistem ini dikembangkan untuk:
1. Meningkatkan kualitas citra low-light
2. Menjaga detail struktur objek
3. Menghindari over-enhancement
4. Mendukung pemrosesan banyak gambar (batch)

---

## 3. Arsitektur Metode

Pipeline sistem terdiri dari 5 tahap utama:

### 3.1 Structure Modeling
Menggunakan:
- Sobel Operator
- Canny Edge Detection

Fungsi:
- Mengambil informasi tepi dan struktur objek

---

### 3.2 Appearance Modeling
Menggunakan:
- Gaussian Blur
- Weighted Enhancement

Fungsi:
- Meningkatkan kontras global
- Menjaga keseimbangan warna

---

### 3.3 Structure-Guided Enhancement
Fungsi:
- Menggabungkan struktur ke dalam citra
- Edge diperkuat, area datar tetap stabil

---

### 3.4 Frequency Refinement
Menggunakan:
- Fast Fourier Transform (FFT)

Fungsi:
- Meningkatkan detail halus
- Menghindari efek blur

---

### 3.5 Adaptive Gamma Correction
Fungsi:
- Menyesuaikan tingkat kecerahan secara otomatis
- Berdasarkan rata-rata intensitas citra

---

## 4. Struktur Folder
