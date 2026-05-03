# AWS Cost Analyzer

Tool CLI berbasis Python untuk menganalisis dan memantau biaya AWS menggunakan Cost Explorer API. Cocok untuk SRE/DevOps yang ingin visibility penuh terhadap pengeluaran cloud.

## Fitur

- [x] Lihat total biaya bulan ini vs bulan lalu
- [ ] Breakdown biaya per AWS service (EC2, S3, RDS, dst)
- [ ] Filter berdasarkan date range
- [ ] Alert ke Slack jika cost melebihi threshold
- [ ] Export ke CSV / JSON

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
AWS_REGION=ap-southeast-1
AWS_PROFILE=default
COST_THRESHOLD_USD=100.0
LOOKBACK_MONTHS=3
```

> **Penting:** Jangan pernah commit file `.env` ke GitHub. File ini sudah di-exclude di `.gitignore`.

## Cara Pakai

```bash
# Lihat biaya bulan ini
python main.py

# Lihat biaya 3 bulan terakhir
python main.py --months 3

# Breakdown per service
python main.py --breakdown
```

## Contoh Output

```
=== AWS Cost Summary ===
Periode  : April 2026
Total    : $42.31 USD

Bulan lalu (Maret 2026): $38.95 USD
Perubahan: +$3.36 (+8.6%) ⚠️

Top Services:
  EC2       $28.50  (67%)
  S3         $8.20  (19%)
  RDS        $5.61  (13%)
```

## Struktur Project

```
aws-cost-analyzer/
├── main.py               # entry point
├── requirements.txt      # dependencies
├── .env.example          # template konfigurasi
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── config.py         # baca environment variables
│   ├── cost_explorer.py  # wrapper boto3 Cost Explorer API
│   └── formatter.py      # format output ke terminal
└── tests/
    └── test_cost_explorer.py
```

## Relevansi SRE

Tool ini merupakan implementasi sederhana dari **FinOps practice** — sebuah disiplin yang semakin penting di dunia SRE modern. Kemampuan memantau dan menganalisis cloud cost adalah skill yang banyak dicari di industri.

## Lisensi

MIT License — lihat [LICENSE](LICENSE)
