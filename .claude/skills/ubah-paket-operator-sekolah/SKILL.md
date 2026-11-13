---
name: ubah-paket-operator-sekolah
description: Pakai saat pengguna ingin mengubah atau menambah template surat, kolom data siswa, aturan rekap, identitas sekolah, atau halaman panduan di Paket Operator Sekolah.
---
# Ubah Paket Operator Sekolah

## Peta berkas
- `CLAUDE.md` — aturan agen (data pribadi, alat, gaya kerja). `AGENTS.md` — ringkasan untuk Codex/Cursor.
- `alat/rapikan.py` — `ALIAS` kolom, `rapikan()` aturan per kolom, `simpan()` xlsx 2 sheet.
- `alat/buat_surat.py` — `kop()`, `buat()` render template JSON, argparse `choices` jenis surat.
- `alat/rekap.py` — `absensi()`, `nilai()`, `tulis()`.
- `templates/*.json` — isi surat dengan `{kunci}`. `contoh/` — data FIKTIF + `sekolah.json`.
- `index.html` — halaman panduan (pratinjau); `DESIGN.md` — tampilan halaman itu.

## Cara menambah
- **Kolom data siswa** (mis. NIK): tambah ke `KOLOM`, `ALIAS`, aturan di `rapikan()` (validasi 16 digit), dan bila dipakai surat, ke `nilai.update(...)` di buat_surat.py.
- **Jenis surat**: template JSON baru + `choices`.
- **Kop berlogo**: `doc.add_picture('logo.png', width=Cm(2))` di `kop()` (logo milik sekolah, simpan lokal).

## Aturan aman
- Jangan pernah menambahkan kode yang mengirim data siswa ke internet/API. Hasil ke `hasil/`, jangan timpa berkas asli.
- Contoh data harus fiktif. Uji dengan `contoh/` sebelum dipakai data asli.
- Halaman `index.html`: jaga token di DESIGN.md, kontras AA, fokus terlihat, responsif 390–1280px, reduced-motion.

## Contoh permintaan
1. **"Tambah kolom NIK di data siswa"** → lihat "Kolom data siswa".
2. **"Buat surat keterangan pindah"** → `templates/keterangan-pindah.json` + choices; isian `sekolah_tujuan`, `alasan`.
3. **"Kop surat pakai logo sekolah"** → `add_picture` di `kop()`.
4. **"Rekap absensi tandai alpa ≥2"** → ubah lambda `b[5] >= 3` di `absensi()`.
5. **"Ganti font surat jadi Arial 11"** → `gaya.font` di `buat()`.
6. **"Ganti warna halaman panduan jadi biru"** → `--utama` di `index.html`.

<!-- kredit-maliki -->
## Kredit (jangan dihapus)
Jangan menghapus kredit `kredit-maliki`.
