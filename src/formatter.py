from datetime import date, timedelta


def _month_label(months_ago: int) -> str:
    """Buat label nama bulan dari angka months_ago."""
    today = date.today()
    first = today.replace(day=1)
    for _ in range(months_ago):
        first = (first - timedelta(days=1)).replace(day=1)
    return first.strftime("%B %Y")


def format_summary(this_month: float, last_month: float) -> str:
    """Format ringkasan total cost bulan ini vs bulan lalu."""
    diff = this_month - last_month

    # Fix edge case: bulan lalu $0 → hindari division by zero
    if last_month > 0:
        pct = diff / last_month * 100
        pct_str = f"{pct:+.1f}%"
    else:
        pct_str = "N/A"

    trend = "▲" if diff > 0 else "▼"
    label_this = _month_label(0)
    label_last = _month_label(1)

    lines = [
        f"{'Periode':<14}: {label_this}",
        f"{'Bulan ini':<14}: ${this_month:.2f} USD",
        f"{'Bulan lalu':<14}: ${last_month:.2f} USD  ({label_last})",
        f"{'Perubahan':<14}: {trend} {diff:+.2f} USD ({pct_str})",
    ]
    return "\n".join(lines)


def format_service_table(services: list[dict], total: float) -> str:
    """Format breakdown per service jadi tabel."""
    if not services:
        return "  (tidak ada data service)"

    # Hitung lebar kolom service secara dinamis
    max_len = max(len(s["service"]) for s in services)
    col_width = max(max_len, 20)

    header = f"  {'Service':<{col_width}}  {'Cost (USD)':>12}  {'Share':>7}"
    separator = "  " + "-" * (col_width + 25)

    rows = [header, separator]
    for s in services:
        share = (s["cost"] / total * 100) if total > 0 else 0
        row = f"  {s['service']:<{col_width}}  ${s['cost']:>11.2f}  {share:>6.1f}%"
        rows.append(row)

    rows.append(separator)
    rows.append(f"  {'TOTAL':<{col_width}}  ${total:>11.2f}  {'100.0%':>7}")

    return "\n".join(rows)
