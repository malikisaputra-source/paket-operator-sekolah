# kredit-maliki: Template oleh Maliki Saputra (@malikisaputra) — https://malikisaputra.biz.id. Lisensi Nonkomersial Maliki Studio: wajib kredit, dilarang dijual (lihat LICENSE).
"""Rapikan data siswa dari CSV/XLSX: nama Title Case, JK L/P, tanggal YYYY-MM-DD,
kelas seragam, HP 08xx, NISN 10 digit, cari duplikat. Hasil: hasil/siswa-rapi.xlsx + laporan masalah.
Pakai: python3 alat/rapikan.py contoh/siswa-mentah.csv
Semua diproses LOKAL. Tidak ada data yang dikirim ke internet."""
import csv, re, sys, datetime
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill

ROMAWI = {"VII": "7", "VIII": "8", "IX": "9", "X": "10", "XI": "11", "XII": "12"}
KOLOM = ["Nama Lengkap", "NISN", "JK", "Tempat Lahir", "Tanggal Lahir", "Kelas", "Nama Ayah", "No HP Ortu"]
ALIAS = {"nama": "Nama Lengkap", "nama lengkap": "Nama Lengkap", "nama siswa": "Nama Lengkap", "nisn": "NISN",
         "jk": "JK", "jenis kelamin": "JK", "l/p": "JK", "tempat lahir": "Tempat Lahir", "tgl lahir": "Tanggal Lahir",
         "tanggal lahir": "Tanggal Lahir", "kelas": "Kelas", "rombel": "Kelas", "nama ayah": "Nama Ayah",
         "no hp ortu": "No HP Ortu", "hp ortu": "No HP Ortu", "no hp": "No HP Ortu"}


def baca(path):
    p = Path(path)
    if p.suffix.lower() in (".xlsx", ".xlsm"):
        ws = load_workbook(p, data_only=True).active
        rows = [[("" if c is None else c) for c in r] for r in ws.iter_rows(values_only=True)]
    else:
        teks = p.read_text(encoding="utf-8-sig")
        dial = csv.Sniffer().sniff(teks.splitlines()[0], delimiters=",;\t")
        rows = list(csv.reader(teks.splitlines(), dial))
    kepala = [ALIAS.get(str(h).strip().lower(), str(h).strip()) for h in rows[0]]
    return [dict(zip(kepala, r)) for r in rows[1:] if any(str(x).strip() for x in r)]


def judul(s):
    s = re.sub(r"\s+", " ", str(s)).strip()
    return " ".join(w.capitalize() for w in s.split(" "))


def tanggal(v):
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.strftime("%Y-%m-%d"), None
    s = str(v).strip()
    for pola in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"):
        try:
            return datetime.datetime.strptime(s, pola).strftime("%Y-%m-%d"), None
        except ValueError:
            pass
    return s, f"tanggal lahir tidak valid: '{s}'"


def kelas(v):
    s = str(v).upper().replace(" ", "").replace("-", "")
    m = re.match(r"^(XII|XI|IX|X|VIII|VII|\d{1,2})([A-Z]?)$", s)
    if not m:
        return str(v).strip(), f"format kelas aneh: '{v}'"
    return ROMAWI.get(m.group(1), m.group(1)) + m.group(2), None


def hp(v):
    d = re.sub(r"\D", "", str(v))
    if d.startswith("62"):
        d = "0" + d[2:]
    if not d:
        return "", "no HP kosong"
    return d, (None if re.match(r"^08\d{8,11}$", d) else f"no HP mencurigakan: '{v}'")


def rapikan(baris):
    hasil, masalah = [], []
    for i, b in enumerate(baris, start=2):
        r, catat = {}, []
        r["Nama Lengkap"] = judul(b.get("Nama Lengkap", ""))
        nisn = re.sub(r"\D", "", str(b.get("NISN", "")))
        if len(nisn) == 9:
            nisn = "0" + nisn  # nol depan hilang karena Excel
        if len(nisn) != 10:
            catat.append(f"NISN bukan 10 digit: '{b.get('NISN')}'")
        r["NISN"] = nisn
        jk = str(b.get("JK", "")).strip().upper()
        r["JK"] = "L" if jk.startswith("L") else "P" if jk.startswith("P") else ""
        if not r["JK"]:
            catat.append("JK kosong/tidak dikenal")
        r["Tempat Lahir"] = judul(b.get("Tempat Lahir", ""))
        r["Tanggal Lahir"], e = tanggal(b.get("Tanggal Lahir", ""))
        e and catat.append(e)
        r["Kelas"], e = kelas(b.get("Kelas", ""))
        e and catat.append(e)
        r["Nama Ayah"] = judul(b.get("Nama Ayah", ""))
        if not r["Nama Ayah"]:
            catat.append("nama ayah kosong")
        r["No HP Ortu"], e = hp(b.get("No HP Ortu", ""))
        e and catat.append(e)
        hasil.append(r)
        masalah += [(i, r["Nama Lengkap"], c) for c in catat]
    lihat = {}
    for i, r in enumerate(hasil, start=2):
        k = r["NISN"] or r["Nama Lengkap"].lower()
        if k in lihat:
            masalah.append((i, r["Nama Lengkap"], f"kemungkinan duplikat baris {lihat[k]}"))
        else:
            lihat[k] = i
    return hasil, masalah


def simpan(hasil, masalah, keluar):
    wb = Workbook()
    ws = wb.active
    ws.title = "Siswa"
    ws.append(["No"] + KOLOM)
    for n, r in enumerate(hasil, 1):
        ws.append([n] + [r[k] for k in KOLOM])
    for c in ws[1]:
        c.font = Font(bold=True)
    for col in "CDEFGHI":
        ws.column_dimensions[col].width = 18
    ws.column_dimensions["B"].width = 26
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        for c in row:
            c.number_format = "@"  # NISN sebagai teks agar nol depan aman
    wm = wb.create_sheet("Perlu Dicek")
    wm.append(["Baris asal", "Nama", "Masalah"])
    kuning = PatternFill("solid", fgColor="FFF3C4")
    for m in masalah:
        wm.append(list(m))
        for c in wm[wm.max_row]:
            c.fill = kuning
    wm.column_dimensions["B"].width = 24
    wm.column_dimensions["C"].width = 48
    wb.save(keluar)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Pakai: python3 alat/rapikan.py <berkas.csv|xlsx> [keluar.xlsx]")
    keluar = Path(sys.argv[2] if len(sys.argv) > 2 else "hasil/siswa-rapi.xlsx")
    keluar.parent.mkdir(parents=True, exist_ok=True)
    hasil, masalah = rapikan(baca(sys.argv[1]))
    simpan(hasil, masalah, keluar)
    print(f"{len(hasil)} siswa dirapikan -> {keluar}")
    print(f"{len(masalah)} hal perlu dicek manual (sheet 'Perlu Dicek'):")
    for m in masalah:
        print(f"  baris {m[0]} {m[1]}: {m[2]}")
