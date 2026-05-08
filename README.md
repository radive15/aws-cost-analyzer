# AWS Cost Analyzer

Tool CLI berbasis Python untuk menganalisis dan memantau biaya AWS menggunakan Cost Explorer API. Cocok untuk SRE/DevOps yang ingin visibility penuh terhadap pengeluaran cloud.

## Fitur

- [x] Lihat total biaya bulan ini vs bulan lalu (dalam USD dan IDR)
- [x] Breakdown biaya per AWS service (EC2, S3, RDS, dst)
- [x] Filter berdasarkan bulan dengan flag `--months`
- [x] Konversi otomatis USD ke IDR dengan kurs live
- [x] Export ke CSV dan JSON dengan flag `--export`
- [x] Visualisasi bar chart per service dengan flag `--chart`
- [ ] Alert ke Slack jika cost melebihi threshold

## Prasyarat

- Python 3.11+
- AWS account dengan akses ke **Cost Explorer**
- IAM permission: `ce:GetCostAndUsage`
- AWS credentials sudah dikonfigurasi (`aws configure`)

## Instalasi

```bash
# 1. Clone repo
git clone https://github.com/rifki/aws-cost-analyzer.git
cd aws-cost-analyzer

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup environment variables
cp .env.example .env
# Edit .env sesuai kebutuhanmu
```

## Konfigurasi

Edit file `.env`:

```env
AWS_PROFILE=default
COST_THRESHOLD_USD=100.0
```

> **Catatan:** `AWS_REGION` tidak perlu diisi — Cost Explorer API AWS selalu menggunakan `us-east-1` untuk semua akun, bukan region spesifik kamu.

> **Penting:** Jangan pernah commit file `.env` ke GitHub. File ini sudah di-exclude di `.gitignore`.

## Cara Pakai

```bash
# Lihat biaya bulan ini + breakdown per service
python main.py

# Lihat biaya bulan lalu
python main.py --months 1

# Lihat biaya 2 bulan yang lalu
python main.py --months 2

# Export hasil ke CSV
python main.py --export csv

# Export hasil ke JSON
python main.py --export json

# Export ke CSV dan JSON sekaligus
python main.py --export all

# Simpan bar chart per service ke file PNG
python main.py --chart

# Kombinasi: export semua format + chart, untuk bulan lalu
python main.py --months 1 --export all --chart

# Lihat help
python main.py --help
```

## Contoh Output

```
=== AWS Cost Analyzer ===

Periode       : May 2026
Bulan ini     : $42.31 USD  (Rp       692,209)
Bulan lalu    : $38.95 USD  (Rp       637,418)  (April 2026)
Perubahan     : ▲ +3.36 USD (+8.6%)

Breakdown per Service:
  Service                    USD          IDR   Share
  ---------------------------------------------------
  Amazon EC2             $ 28.50   Rp  466,575   67.3%
  Amazon S3              $  8.20   Rp  134,218   19.4%
  Amazon RDS             $  5.61   Rp   91,821   13.3%
  ---------------------------------------------------
  TOTAL                  $ 42.31   Rp  692,209  100.0%

CSV   → aws-cost-2026-05.csv
JSON  → aws-cost-2026-05.json
Chart → aws-cost-2026-05.png
```

## Struktur Project

```
aws-cost-analyzer/
├── main.py               # entry point + CLI argument parser
├── requirements.txt      # dependencies
├── .env.example          # template konfigurasi
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── config.py         # baca environment variables
│   ├── cost_explorer.py  # wrapper boto3 Cost Explorer API
│   ├── currency.py       # ambil kurs live USD ke IDR
│   ├── formatter.py      # format output tabel ke terminal
│   ├── exporter.py       # export data ke CSV dan JSON
│   └── visualizer.py     # buat bar chart PNG dengan matplotlib
└── tests/
    └── test_cost_explorer.py
```

## Relevansi SRE

Tool ini merupakan implementasi sederhana dari **FinOps practice** — sebuah disiplin yang semakin penting di dunia SRE modern. Kemampuan memantau dan menganalisis cloud cost adalah skill yang banyak dicari di industri.

## Lisensi

MIT License — lihat [LICENSE](LICENSE)
