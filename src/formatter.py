from src.utils import get_month_label


def _idr(amount_usd: float, rate: float) -> str:
    """Konversi USD ke string IDR yang diformat."""
    return f"Rp {amount_usd * rate:>13,.0f}"


def format_summary(this_month: float, last_month: float, rate: float) -> str:
    """Format ringkasan total cost bulan ini vs bulan lalu."""
    diff = this_month - last_month
    pct_str = f"{diff / last_month * 100:+.1f}%" if last_month > 0 else "N/A"
    trend = "▲" if diff > 0 else "▼"

    lines = [
        f"{'Periode':<14}: {get_month_label(0)}",
        f"{'Bulan ini':<14}: ${this_month:.2f} USD  ({_idr(this_month, rate)})",
        f"{'Bulan lalu':<14}: ${last_month:.2f} USD  ({_idr(last_month, rate)})  ({get_month_label(1)})",
        f"{'Perubahan':<14}: {trend} {diff:+.2f} USD ({pct_str})",
    ]
    return "\n".join(lines)


def format_service_table(services: list[dict], total: float, rate: float) -> str:
    """Format breakdown per service jadi tabel dengan kolom IDR."""
    if not services:
        return "  (tidak ada data service)"

    col_width = max((len(s["service"]) for s in services), default=20)
    col_width = max(col_width, 20)

    header = f"  {'Service':<{col_width}}  {'USD':>10}  {'IDR':>16}  {'Share':>7}"
    separator = "  " + "-" * (col_width + 40)

    rows = [header, separator]
    for s in services:
        share = (s["cost"] / total * 100) if total > 0 else 0
        row = (
            f"  {s['service']:<{col_width}}"
            f"  ${s['cost']:>9.2f}"
            f"  {_idr(s['cost'], rate):>16}"
            f"  {share:>6.1f}%"
        )
        rows.append(row)

    rows.append(separator)
    rows.append(
        f"  {'TOTAL':<{col_width}}"
        f"  ${total:>9.2f}"
        f"  {_idr(total, rate):>16}"
        f"  {'100.0%':>7}"
    )
    return "\n".join(rows)
