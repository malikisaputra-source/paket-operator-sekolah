# kredit-maliki: Template oleh Maliki Saputra (@malikisaputra) — https://malikisaputra.biz.id. Lisensi Nonkomersial Maliki Studio: wajib kredit, dilarang dijual (lihat LICENSE).
"""Buat surat .docx (keterangan-aktif | izin | undangan) dari templates/<jenis>.json + contoh/sekolah.json.
Pakai:
  python3 alat/buat_surat.py keterangan-aktif --nisn 0101234561 --data hasil/siswa-rapi.xlsx
  python3 alat/buat_surat.py izin --nisn 0101234562 --data hasil/siswa-rapi.xlsx --isi tanggal_izin="14 November 2026" alasan="acara keluarga"
  python3 alat/buat_surat.py undangan --isi perihal="Rapat Orang Tua" hari_tanggal="Sabtu, 21 November 2026" waktu="08.00 WIB" tempat="Aula" acara="Pembagian rapor tengah semester"
Nomor surat diisi --nomor, atau otomatis 'xxx' (WAJIB diganti operator). Diproses LOKAL."""
import argparse, json, re, datetime
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

AKAR = Path(__file__).resolve().parent.parent
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]


def tgl_id(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


def cari_siswa(path, nisn):
    from openpyxl import load_workbook
    ws = load_workbook(path, data_only=True)["Siswa"]
    rows = list(ws.iter_rows(values_only=True))
    kepala = [str(h) for h in rows[0]]
    for r in rows[1:]:
        d = dict(zip(kepala, r))
        if str(d.get("NISN")) == nisn:
            return d
    raise SystemExit(f"NISN {nisn} tidak ditemukan di {path}")


def isi(teks, nilai):
    def ganti(m):
        k = m.group(1)
        if k not in nilai:
            raise SystemExit(f"Isian '{k}' belum ada. Tambahkan --isi {k}=\"...\"")
        return str(nilai[k])
    return re.sub(r"\{(\w+)\}", ganti, teks)


def kop(doc, s):
    for i, (t, ukuran, tebal) in enumerate([("PEMERINTAH KABUPATEN CONTOH — DINAS PENDIDIKAN", 11, False),
                                            (s["nama_sekolah"].upper(), 15, True),
                                            (f'NPSN {s["npsn"]} · {s["alamat"]}', 9.5, False),
                                            (f'Telp. {s["telepon"]} · {s["email"]}', 9.5, False)]):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(t)
        r.font.size = Pt(ukuran)
        r.bold = tebal
    garis = doc.add_paragraph("_" * 86)
    garis.alignment = WD_ALIGN_PARAGRAPH.CENTER


def buat(jenis, nilai, keluar):
    t = json.loads((AKAR / "templates" / f"{jenis}.json").read_text(encoding="utf-8"))
    s = nilai
    doc = Document()
    for sec in doc.sections:
        sec.top_margin, sec.bottom_margin, sec.left_margin, sec.right_margin = Cm(2), Cm(2), Cm(2.5), Cm(2)
    gaya = doc.styles["Normal"]
    gaya.font.name, gaya.font.size = "Times New Roman", Pt(12)
    kop(doc, s)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if t.get("judul") else WD_ALIGN_PARAGRAPH.LEFT
    if t.get("judul"):
        r = p.add_run(t["judul"])
        r.bold, r.underline = True, True
        p.add_run(f"\nNomor: {s['nomor']}")
    else:
        p.add_run(f"Nomor\t: {s['nomor']}\nLampiran\t: -\nPerihal\t: {isi(t['perihal'], s)}")
    for blok in t["isi"]:
        if isinstance(blok, dict):  # tabel data label : nilai
            tb = doc.add_table(rows=0, cols=3)
            for label, kunci in blok["tabel"]:
                c = tb.add_row().cells
                c[0].text, c[1].text, c[2].text = label, ":", str(isi(kunci, s))
                c[0].width, c[1].width = Cm(5), Cm(0.6)
        else:
            q = doc.add_paragraph(isi(blok, s))
            q.paragraph_format.first_line_indent = Cm(1.25) if not blok.startswith(("Yth", "Kepada", "Di ")) else None
            q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    ttd = doc.add_paragraph()
    ttd.paragraph_format.left_indent = Cm(9)
    ttd.add_run(f"{s['kota_surat']}, {s['tanggal_surat']}\nKepala Sekolah,\n\n\n\n")
    ttd.add_run(s["kepala_sekolah"]).bold = True
    ttd.add_run(f"\nNIP. {s['nip_kepala']}")
    doc.save(keluar)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("jenis", choices=["keterangan-aktif", "izin", "undangan"])
    ap.add_argument("--nisn")
    ap.add_argument("--data", default="hasil/siswa-rapi.xlsx")
    ap.add_argument("--sekolah", default=str(AKAR / "contoh" / "sekolah.json"))
    ap.add_argument("--nomor", default="421.3/xxx/SMP/2026")
    ap.add_argument("--isi", nargs="*", default=[], help='kunci="nilai"')
    a = ap.parse_args()
    nilai = json.loads(Path(a.sekolah).read_text(encoding="utf-8"))
    nilai.update(nomor=a.nomor, tanggal_surat=tgl_id(datetime.date.today()))
    if a.nisn:
        sw = cari_siswa(a.data, a.nisn)
        nilai.update(nama=sw["Nama Lengkap"], nisn=sw["NISN"], kelas=sw["Kelas"], jk=sw["JK"],
                     ttl=f'{sw["Tempat Lahir"]}, {sw["Tanggal Lahir"]}', ortu=sw["Nama Ayah"])
    for kv in a.isi:
        k, _, v = kv.partition("=")
        nilai[k] = v
    keluar = Path("hasil") / f"surat-{a.jenis}-{a.nisn or datetime.date.today()}.docx"
    keluar.parent.mkdir(exist_ok=True)
    buat(a.jenis, nilai, keluar)
    print(f"Surat dibuat: {keluar}  (cek nomor surat & isi sebelum dicetak)")
