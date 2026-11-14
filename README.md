# Paket Operator Sekolah — Asisten AI Administrasi

Paket agent/skill (bukan aplikasi web) untuk Claude Code atau Codex: merapikan data siswa dari Excel/CSV, membuat surat (keterangan aktif, izin, undangan) ke Word .docx, dan merekap absensi/nilai. Skrip Python kecil yang bisa diperiksa sendiri.

> **Prototipe — batasan jujur**
> - Ini bukan pengganti Dapodik/aplikasi resmi. Format surat contoh umum, sesuaikan dengan tata naskah dinas daerahmu.
> - **Data siswa = data pribadi anak** (UU 27/2022 PDP). Skrip berjalan lokal dan tidak mengirim data. Namun agen AI (Claude Code/Codex) menjalankan modelnya di server penyedia, jadi isi berkas yang dibaca agen ikut terkirim. Pakai akun yang kebijakannya disetujui sekolah, atau uji dengan data fiktif/disamarkan.
> - Jangan unggah data siswa ke situs, chat AI di browser, atau grup WA.
> - Tanggal/NISN yang salah TIDAK ditebak, hanya ditandai "Perlu Dicek".
> - Surat tetap harus diperiksa dan ditandatangani pejabat berwenang; nomor surat bawaan `xxx`.
> - Butuh Python 3 + `openpyxl` + `python-docx`. Excel lama (.xls) harus disimpan ulang jadi .xlsx/CSV.

## Fitur
- Rapikan nama, JK, tanggal lahir, kelas (VII-B → 7B), HP (+62 → 08), NISN 10 digit
- Tandai data janggal & kemungkinan duplikat di sheet "Perlu Dicek"
- Surat keterangan aktif, izin, undangan orang tua ke .docx dengan kop & tanda tangan
- Template surat JSON, mudah ditambah
- Rekap absensi H/S/I/A + persen hadir, tandai alpa ≥3
- Rekap nilai: rata-rata, peringkat, mapel di bawah KKM
- CLAUDE.md + 3 skill kerja + skill ubah paket
- Contoh data fiktif di `contoh/`

## Cara menjalankan
1. Pasang Python 3 (python.org), lalu di terminal: `pip install openpyxl python-docx`.
2. Ekstrak ZIP, isi `contoh/sekolah.json` dengan identitas sekolahmu.
3. Pasang Claude Code (claude.com/claude-code) atau Codex, buka terminal di folder paket, jalankan `claude`.
4. Coba dulu dengan data contoh: "rapikan contoh/siswa-mentah.csv", "buat surat keterangan aktif untuk NISN 0101234561", "rekap nilai contoh/nilai-7a-ganjil.csv".
5. Hasil ada di folder `hasil/`. Tanpa AI pun bisa: jalankan perintah di bagian atas tiap skrip `alat/*.py`.

## Struktur folder
```
CLAUDE.md, AGENTS.md          aturan agen
.claude/skills/               rapikan-data-siswa, buat-surat, rekap-absensi-nilai, ubah-paket-operator-sekolah
alat/                         rapikan.py, buat_surat.py, rekap.py
templates/                    keterangan-aktif.json, izin.json, undangan.json
contoh/                       data FIKTIF + sekolah.json
index.html                    halaman panduan (pratinjau)
hasil/                        keluaran (diabaikan git)
```

## Ubah brand/warna
Surat: font & margin di `buat()` (`alat/buat_surat.py`), kop di `kop()`. Halaman panduan: `--utama`/`--aksen` di `index.html` (lihat `DESIGN.md`).

## Ubah pakai Claude
- **Claude Code / Claude Desktop:** buka folder paket, skill di `.claude/skills` terbaca otomatis.
- **claude.ai:** unggah ZIP skill (tombol "Unduh Skill" di malikisaputra.biz.id/kode) lewat Customize › Skills › "+" › Create skill › Upload a skill (folder skill sebagai akar ZIP). Syarat: "Code execution and file creation" aktif di Settings › Capabilities (Free/Pro/Max); di Team/Enterprise diatur Owner. Sumber: support.claude.com/en/articles/12512180 (dicek 6 Nov 2026). Ingat: di claude.ai berkas diunggah ke server, jadi JANGAN pakai data siswa asli di sana.

## Mau hasil lebih maksimal?
- impeccable — https://github.com/pbakaus/impeccable (Apache-2.0, dicek 6 Nov 2026)
- ui-ux-pro-max — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (MIT menurut GitHub API, dicek 6 Nov 2026)

## Lisensi
Lisensi Nonkomersial Maliki Studio (kredit wajib, dilarang dijual) (lihat `LICENSE`).

Dibuat oleh Maliki Studio — malikisaputra.biz.id, follow TikTok/IG @malikisaputra

<!-- panduan-ai-maliki -->
## Ubah sendiri sesuai kebutuhanmu pakai AI

Kamu tidak perlu jago coding. Template ini sudah disiapkan supaya mudah diubah AI: ada **AGENTS.md** (aturan proyek untuk AI), **DESIGN.md** (gaya desain), dan skill Claude di folder `.claude/skills/`. Pilih salah satu cara di bawah.

### Cara 1: ChatGPT, Claude, atau Gemini di browser (paling gampang, gratis)
1. Unduh ZIP template ini, lalu ekstrak.
2. Buka chatgpt.com, claude.ai, atau gemini.google.com.
3. Unggah berkas yang mau diubah (biasanya `index.html`, `style.css`, `app.js`, atau berkas data). Unggah juga `AGENTS.md` dan `DESIGN.md` (kalau ada) biar AI paham aturannya. ChatGPT juga bisa menerima ZIP utuh.
4. Tulis permintaanmu (contoh di bawah), lalu minta: "Kirim ulang berkas yang diubah secara utuh."
5. Ganti berkas lama dengan hasil dari AI, lalu buka `index.html` di browser untuk cek.

### Cara 2: Claude Code (paling rapi untuk perubahan besar)
1. Pasang Claude Code (lihat claude.com/claude-code), atau pakai aplikasi Claude Desktop tab Code.
2. Buka folder template ini, lalu jalankan `claude` di terminal folder itu.
3. Tulis permintaanmu. Kalau ada folder `.claude/skills/ubah-…`, Claude Code otomatis memakainya, jadi hasilnya tetap mengikuti desain aslinya.

### Cara 3: Codex (OpenAI)
1. Pasang Codex CLI atau pakai Codex di aplikasi ChatGPT.
2. Buka folder template, jalankan `codex`. Codex otomatis membaca `AGENTS.md`.
3. Tulis permintaanmu, cek perubahannya, lalu setujui.

### Cara 4: Google Antigravity atau Gemini CLI (gratis)
1. Antigravity: buka aplikasinya, pilih **Open Folder** ke folder template ini, lalu tulis permintaan di panel agen.
2. Gemini CLI: jalankan `gemini` di folder template.
3. Di awal, tulis: "Baca AGENTS.md dan DESIGN.md dulu sebelum mengubah apa pun."

### Contoh permintaan yang bisa langsung kamu pakai
- "Ganti nama, logo teks, dan warna utama jadi hijau tua sesuai usahaku: [nama usaha]."
- "Tambahkan kolom [nama kolom] di formulir dan tampilkan di daftar."
- "Ubah semua data contoh jadi data usahaku: [tempel datanya]."
- "Tambahkan halaman/menu baru untuk [kebutuhan], gaya desainnya sama dengan yang sudah ada."
- "Jelaskan dulu cara kerja aplikasi ini dengan bahasa sederhana, baru ubah [bagian]."

### Tips biar hasilnya bagus
- Satu permintaan = satu perubahan. Cek dulu hasilnya, baru minta yang berikutnya.
- Simpan salinan folder asli sebelum mengubah, jadi bisa balik kalau ada yang rusak.
- Kalau ada error, salin pesan errornya (klik kanan > Inspect > Console) lalu tempel ke AI.
- Data aplikasi tersimpan di browser (localStorage). Backup dulu sebelum ganti versi.
- Jangan hapus kredit "Template oleh @malikisaputra", dan template ini **tidak boleh diperjualbelikan** tanpa izin. Mau menjual atau kerja sama? Diskusikan dulu dengan kreatornya (@malikisaputra).

Masih bingung? Komen di TikTok/IG **@malikisaputra**, nanti aku bantu.
