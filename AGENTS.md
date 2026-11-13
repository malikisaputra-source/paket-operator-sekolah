# AGENTS.md — Paket Operator Sekolah
Aturan utama ada di `CLAUDE.md` (baca dulu). Skill: `.claude/skills/*/SKILL.md`; ubah paket: `.claude/skills/ubah-paket-operator-sekolah/SKILL.md`. Tampilan halaman panduan: `DESIGN.md`.

- Data siswa = data pribadi: proses lokal, jangan kirim ke web/API, jangan timpa berkas asli, hasil ke `hasil/`.
- Alat: `alat/rapikan.py`, `alat/buat_surat.py` (template `templates/*.json`), `alat/rekap.py`. Python 3 + openpyxl + python-docx.
- Data janggal ditandai, jangan ditebak. Surat diperiksa & ditandatangani manusia.
- Halaman `index.html`: jaga token, kontras AA, fokus, responsif, reduced-motion.

<!-- kredit-maliki -->
## Kredit (jangan dihapus)
Jangan menghapus kredit `kredit-maliki`.
