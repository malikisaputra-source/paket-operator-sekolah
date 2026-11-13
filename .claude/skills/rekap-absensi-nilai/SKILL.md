---
name: rekap-absensi-nilai
description: Pakai saat operator/wali kelas ingin merekap absensi bulanan (hadir, sakit, izin, alpa, persen hadir) atau nilai (rata-rata, peringkat, mapel di bawah KKM) dari CSV ke Excel.
---
# Rekap absensi & nilai

## Format masukan
- Absensi: CSV kolom `NISN, Nama, <tanggal...>` isi H/S/I/A (lihat `contoh/absensi-7a-oktober.csv`).
- Nilai: CSV kolom `NISN, Nama, <mapel...>` angka (lihat `contoh/nilai-7a-ganjil.csv`).
Bila sumbernya Excel, simpan dulu sebagai CSV atau ubah `baca()` di `alat/rekap.py` memakai openpyxl.

## Langkah
1. `python3 alat/rekap.py absensi <csv>` atau `python3 alat/rekap.py nilai <csv> --kkm <angka>` (KKM dari `contoh/sekolah.json` bila ada).
2. Laporkan ringkas: siswa alpa ≥3 (perlu ditindaklanjuti wali kelas), siswa dengan mapel di bawah KKM, rata-rata kelas. Jangan memberi label negatif pada siswa; pakai bahasa netral ("perlu pendampingan").
3. Keluaran di `hasil/rekap-*.xlsx`, baris merah = perlu perhatian.
