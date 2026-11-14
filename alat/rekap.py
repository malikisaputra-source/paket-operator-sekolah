# kredit-maliki: Template oleh Maliki Saputra (@malikisaputra) — https://malikisaputra.biz.id. Lisensi Nonkomersial Maliki Studio: wajib kredit, dilarang dijual (lihat LICENSE).
"""Rekap absensi (H/S/I/A per siswa, % hadir) atau nilai (rata-rata, peringkat, di bawah KKM) ke .xlsx.
Pakai:
  python3 alat/rekap.py absensi contoh/absensi-7a-oktober.csv
  python3 alat/rekap.py nilai contoh/nilai-7a-ganjil.csv --kkm 75
Diproses LOKAL."""
import argparse, csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill


def baca(p):
    with open(p, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def tulis(keluar, kepala, baris, tandai=None):
    wb = Workbook()
    ws = wb.active
    ws.append(kepala)
    for c in ws[1]:
        c.font = Font(bold=True)
    merah = PatternFill("solid", fgColor="FDE2E2")
    for b in baris:
        ws.append(b)
        if tandai and tandai(b):
            for c in ws[ws.max_row]:
                c.fill = merah
    ws.column_dimensions["B"].width = 24
    wb.save(keluar)


def absensi(path):
    data = baca(path)
    hari = [k for k in data[0] if k not in ("NISN", "Nama")]
    baris = []
    for d in data:
        n = {x: sum(1 for h in hari if d[h].strip().upper() == x) for x in "HSIA"}
        baris.append([d["NISN"], d["Nama"], n["H"], n["S"], n["I"], n["A"], round(n["H"] / len(hari) * 100, 1)])
    return ["NISN", "Nama", "Hadir", "Sakit", "Izin", "Alpa", "% Hadir"], baris, lambda b: b[5] >= 3, f"{len(hari)} hari efektif; merah = alpa ≥3"


def nilai(path, kkm):
    data = baca(path)
    mapel = [k for k in data[0] if k not in ("NISN", "Nama")]
    baris = []
    for d in data:
        v = [float(d[m]) for m in mapel]
        bawah = [m for m, x in zip(mapel, v) if x < kkm]
        baris.append([d["NISN"], d["Nama"], *v, round(sum(v) / len(v), 2), 0, ", ".join(bawah) or "-"])
    urut = sorted(baris, key=lambda b: -b[-3])
    for i, b in enumerate(urut, 1):
        b[-2] = i
    return ["NISN", "Nama", *mapel, "Rata-rata", "Peringkat", f"Di bawah KKM {kkm}"], baris, lambda b: b[-1] != "-", f"KKM {kkm}; merah = ada mapel di bawah KKM"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("jenis", choices=["absensi", "nilai"])
    ap.add_argument("berkas")
    ap.add_argument("--kkm", type=float, default=75)
    a = ap.parse_args()
    kepala, baris, tandai, ket = absensi(a.berkas) if a.jenis == "absensi" else nilai(a.berkas, a.kkm)
    keluar = Path("hasil") / f"rekap-{Path(a.berkas).stem}.xlsx"
    keluar.parent.mkdir(exist_ok=True)
    tulis(keluar, kepala, baris, tandai)
    print(f"Rekap -> {keluar} ({ket})")
    for b in baris:
        print("  ", b)
