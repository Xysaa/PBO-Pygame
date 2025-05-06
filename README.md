# PBO-Pygame: OOP Game Repository

Selamat datang di repository **PBO-Pygame**, proyek game berbasis OOP menggunakan Python dan Pygame. Proyek ini dikembangkan secara berkelompok oleh mahasiswa Teknik Informatika untuk memenuhi tugas mata kuliah.

---

## 🎮 Deskripsi Proyek

PBO-Pygame adalah game 2D sederhana yang menerapkan prinsip **Pemrograman Berorientasi Objek (PBO)** dan menggunakan **Pygame** untuk rendering dan manajemen event. Struktur modular memungkinkan tiap anggota tim bekerja pada fitur masing-masing tanpa konflik.

---

## 🚀 Persiapan Lingkungan

1. **Clone Repository**
   ```bash
   git clone https://github.com/Xysaa/PBO-Pygame.git
   cd PBO-Pygame
   ```

2. **Buat Virtual Environment (Opsional tapi Direkomendasikan)**
   ```bash
   python -m venv venv
   source venv/bin/activate     # Linux/macOS
   venv\\Scripts\\activate    # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🌿 Struktur Cabang (Branch)

Kami menggunakan _Git Flow_ sederhana:

- **`main`**: Cabang utama. Hanya berisi kode yang sudah stabil dan teruji.
- **`feature/xxx`**: Cabang untuk pengembangan fitur baru. Nama cabang sebaiknya menggambarkan fitur, misalnya `feature/player-movement`.
- **`hotfix/xxx`**: Cabang untuk perbaikan bug kritis.

---

## 🔄 Alur Kerja Git

Berikut panduan step-by-step bagi anggota tim baru untuk berkontribusi:

### 1. Pastikan Cabang `main` Terupdate

```bash
# Pindah ke main
git checkout main
# Ambil perubahan terbaru
git pull origin main
```

### 2. Membuat Cabang Fitur Baru

```bash
# Buat dan pindah ke branch baru
git checkout -b feature/namafitur
```

Contoh:
```bash
git checkout -b feature/enemy-behavior
```

### 3. Lakukan Perubahan dan Commit

1. Modifikasi atau tambahkan file sesuai fitur.
2. Tambahkan perubahan ke staging area:
   ```bash
   git add path/to/file.py
   # atau untuk semua file
   git add .
   ```
3. Commit dengan pesan yang jelas:
   ```bash
   git commit -m "[FEATURE] Implementasi pergerakan musuh"
   ```

> **Tip:** Gunakan awalan `[FEATURE]`, `[FIX]`, `[DOC]`, dsb.

### 4. Push Cabang ke Remote

```bash
# Push branch ke GitHub dan set upstream
git push -u origin feature/namafitur
```

### 5. Membuat Pull Request (PR)

1. Buka repository di GitHub: https://github.com/Xysaa/PBO-Pygame
2. Klik tab **Pull requests**, lalu **New pull request**.
3. Pada opsi **base**, pilih `main`. Pada opsi **compare**, pilih `feature/namafitur`.
4. Isi judul dan deskripsi PR:
   - Judul ringkas tapi menjelaskan fitur.
   - Deskripsi detail perubahan dan cara mengetes.
5. Klik **Create pull request**.

> **Tip:** Tandai anggota tim lain sebagai reviewer.

### 6. Menarik Perubahan (Pull) dari `main`

Sebelum memulai pekerjaan baru, selalu sinkron dengan main:

```bash
git checkout main
git pull origin main
```

Jika di feature branch perlu menggabungkan perubahan terbaru dari main:

```bash
# Dari dalam feature branch
git checkout feature/namafitur
git pull origin main
# atau menggunakan rebase
# git rebase main
```

---

## ✅ Checklist Kontribusi

- [ ] Membuat branch dengan naming convention yang benar.
- [ ] Commit dengan pesan jelas sesuai kategori.
- [ ] Push branch dan buat PR sebelum tenggat.
- [ ] Menambahkan dokumentasi (jika diperlukan) di `docs/`.
- [ ] Memastikan semua test (jika ada) lulus.

---


Selamat berkontribusi!
