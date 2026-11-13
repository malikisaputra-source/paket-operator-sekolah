---
name: buat-surat
description: Pakai saat operator sekolah minta dibuatkan surat keterangan aktif belajar, surat izin tidak masuk, atau surat undangan orang tua dalam format Word (.docx) dari data siswa dan template.
---
# Buat surat sekolah (.docx)

## Langkah
1. Pastikan `contoh/sekolah.json` sudah berisi identitas sekolah asli (nama, NPSN, alamat, kepala sekolah, NIP). Bila masih "Contoh", ingatkan operator.
2. Pastikan data siswa sudah rapi (`hasil/siswa-rapi.xlsx`; bila belum, jalankan skill rapikan-data-siswa).
3. Tanyakan yang belum ada: jenis surat, NISN siswa, nomor surat, dan isian khusus:
   - `keterangan-aktif`: cukup `--nisn`.
   - `izin`: `--nisn`, `tanggal_izin`, `alasan`.
   - `undangan`: `perihal`, `hari_tanggal`, `waktu`, `tempat`, `acara` (tanpa NISN).
4. Jalankan, contoh: `python3 alat/buat_surat.py izin --nisn 0101234562 --nomor "421.3/045/SMP/2026" --isi tanggal_izin="14 November 2026" alasan="acara keluarga"`.
5. Laporkan nama berkas di `hasil/`. Ingatkan: periksa nomor surat (bawaan `xxx`), kop, tanda tangan & stempel basah/elektronik resmi. Banyak siswa sekaligus: ulangi per NISN.

## Menambah jenis surat
Buat `templates/<jenis>.json` (`judul` atau `perihal`, `isi`: daftar paragraf berisi `{kunci}` dan objek `{"tabel": [[label, "{kunci}"]]}`), lalu tambahkan nama jenis di `choices` argparse di `alat/buat_surat.py`.
