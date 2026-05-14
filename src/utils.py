# src/utils.py
from datetime import date, timedelta


def get_period_label(months_ago: int) -> str:
    """Hasilkan label periode format YYYY-MM (untuk nama file)."""
    today = date.today()
    first = today.replace(day=1)
    for _ in range(months_ago):
        first = (first - timedelta(days=1)).replace(day=1)
    return first.strftime("%Y-%m")


def get_month_label(months_ago: int) -> str:
    """Hasilkan label periode format 'January 2025' (untuk display)."""
    today = date.today()
    first = today.replace(day=1)
    for _ in range(months_ago):
        first = (first - timedelta(days=1)).replace(day=1)
    return first.strftime("%B %Y")
