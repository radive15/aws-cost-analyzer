import argparse
import logging

from src.cost_explorer import get_cost_by_service, get_monthly_cost
from src.currency import get_usd_to_idr
from src.exporter import export_to_csv, export_to_json
from src.formatter import format_service_table, format_summary
from src.visualizer import save_chart


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="AWS Cost Analyzer")
    parser.add_argument(
        "--months",
        type=int,
        default=0,
        help="Bulan ke belakang (0=bulan ini, 1=bulan lalu)",
    )
    parser.add_argument(
        "--export",
        choices=["csv", "json", "all"],
        help="Export hasil ke file: csv, json, atau all (keduanya)",
    )
    parser.add_argument(
        "--chart",
        action="store_true",
        help="Simpan bar chart per service ke file PNG",
    )

    args = parser.parse_args()

    print("\n=== AWS Cost Analyzer ===\n")

    # Ambil exchange rate sekali — bukan per baris output
    rate = get_usd_to_idr()

    this_month = get_monthly_cost(months_ago=args.months)
    last_month = get_monthly_cost(months_ago=args.months + 1)
    services = get_cost_by_service(months_ago=args.months)

    print(format_summary(this_month, last_month, rate))
    print("\nBreakdown per Service:")
    print(format_service_table(services, this_month, rate))
    print()

    # Export jika flag --export diberikan
    if args.export in ("csv", "all"):
        path = export_to_csv(services, this_month, rate, months_ago=args.months)
        print(f"CSV  → {path}")

    if args.export in ("json", "all"):
        path = export_to_json(services, this_month, last_month, rate, months_ago=args.months)
        print(f"JSON → {path}")

    if args.chart:
        path = save_chart(services, this_month, rate, months_ago=args.months)
        print(f"Chart → {path}")

if __name__ == "__main__":
    main()
