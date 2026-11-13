---
name: rapikan-data-siswa
description: Pakai saat operator sekolah ingin merapikan, membersihkan, atau memvalidasi data siswa dari Excel/CSV (nama acak huruf besar-kecil, NISN hilang nol depan, tanggal lahir beda format, kelas VII-B/7 b, nomor HP +62, data dobel).
---
# Rapikan data siswa

Data siswa = data pribadi. Proses lokal saja, jangan diunggah atau dikirim ke web.

## Langkah
1. Tanyakan/temukan berkas masukan (CSV `,`/`;` atau .xlsx). Jangan ubah berkas aslinya.
2. Cek kolom: skrip mengenali alias (Nama/Nama Siswa, JK/Jenis Kelamin, Tgl Lahir, Rombel, HP Ortu). Bila kolom lain, tambahkan ke `ALIAS` di `alat/rapikan.py`.
3. Jalankan `python3 alat/rapikan.py <berkas> hasil/siswa-rapi.xlsx`.
4. Laporkan ringkas: jumlah siswa, daftar "Perlu Dicek" (NISN bukan 10 digit, tanggal tidak valid, kosong, duplikat). JANGAN menebak data yang salah (mis. tanggal 30 Februari): minta operator mengecek dokumen asli (akta/rapor/Dapodik).
5. Ingatkan: NISN disimpan sebagai teks agar nol depan tidak hilang; jangan ubah kolom jadi Number di Excel.

## Aturan rapikan
Nama Title Case & spasi tunggal; JK → L/P; tanggal → YYYY-MM-DD (format d/m/Y, d-m-Y, Y-m-d); kelas romawi → angka (VII-B → 7B); HP → 08xxxxxxxxxx; NISN 9 digit diberi nol depan.
