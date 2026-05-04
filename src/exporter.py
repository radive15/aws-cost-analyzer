import csv
import json
import logging
from datetime import date, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


def _get_period_label(months_ago: int) -> str:
    """Hasilkan label periode format YYYY-MM."""
    today = date.today()
    first = today.replace(day=1)
    for _ in range(months_ago):
        first = (first - timedelta(days=1)).replace(day=1)
    return first.strftime("%Y-%m")


def export_to_csv(
    services: list[dict],
    total_usd: float,
    rate: float,
    months_ago: int = 0,
    output_dir: str = ".",
) -> str:
    """
    Export breakdown per service ke file CSV.

    Args:
        services: List of {"service": str, "cost": float}
        total_usd: Total cost dalam USD
        rate: Exchange rate USD ke IDR
        months_ago: 0 = bulan ini, 1 = bulan lalu
        output_dir: Folder tujuan file CSV

    Returns:
        Path lengkap file CSV yang dibuat
    """
    period = _get_period_label(months_ago)
    filename = Path(output_dir) / f"aws-cost-{period}.csv"

    # open() pakai context manager (with) — file pasti ditutup meski ada error
    # ini setara dengan "guaranteed cleanup" seperti defer di Go
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["service", "cost_usd", "cost_idr", "share_pct"]
            )
            writer.writeheader()

            for s in services:
                share = (s["cost"] / total_usd * 100) if total_usd > 0 else 0.0
                writer.writerow({
                    "service": s["service"],
                    "cost_usd": round(s["cost"], 4),
                    "cost_idr": round(s["cost"] * rate),
                    "share_pct": round(share, 2),
                })

        logger.info(f"CSV disimpan: {filename}")
        return str(filename)

    except OSError as e:
        logger.error(f"Gagal menulis CSV ke {filename}: {e}")
        raise


def export_to_json(
    services: list[dict],
    this_month: float,
    last_month: float,
    rate: float,
    months_ago: int = 0,
    output_dir: str = ".",
) -> str:
    """
    Export summary + breakdown per service ke file JSON.

    Args:
        services: List of {"service": str, "cost": float}
        this_month: Total cost bulan ini dalam USD
        last_month: Total cost bulan lalu dalam USD
        rate: Exchange rate USD ke IDR
        months_ago: 0 = bulan ini, 1 = bulan lalu
        output_dir: Folder tujuan file JSON

    Returns:
        Path lengkap file JSON yang dibuat
    """
    period = _get_period_label(months_ago)
    filename = Path(output_dir) / f"aws-cost-{period}.json"

    diff = this_month - last_month
    change_pct = round(diff / last_month * 100, 2) if last_month > 0 else None

    data = {
        "period": period,
        "exchange_rate_usd_idr": rate,
        "summary": {
            "total_usd": round(this_month, 4),
            "total_idr": round(this_month * rate),
            "last_month_usd": round(last_month, 4),
            "change_usd": round(diff, 4),
            "change_pct": change_pct,
        },
        # list comprehension — cara Pythonic membuat list baru dari list lain
        "services": [
            {
                "service": s["service"],
                "cost_usd": round(s["cost"], 4),
                "cost_idr": round(s["cost"] * rate),
                "share_pct": round((s["cost"] / this_month * 100) if this_month > 0 else 0.0, 2),
            }
            for s in services
        ],
    }

    try:
        with open(filename, "w", encoding="utf-8") as f:
            # indent=2 supaya JSON-nya human-readable, bukan satu baris
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"JSON disimpan: {filename}")
        return str(filename)

    except OSError as e:
        logger.error(f"Gagal menulis JSON ke {filename}: {e}")
        raise
