# main.py
import argparse
import logging

from src.cost_explorer import get_cost_by_service, get_monthly_cost
from src.formatter import format_service_table, format_summary

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
        help="Bulan ke belakang yang ingin dianalisis (0=bulan ini, 1=bulan lalu)",
    )
    args = parser.parse_args()

    print("\n=== AWS Cost Analyzer ===\n")

    this_month = get_monthly_cost(months_ago=args.months)
    last_month = get_monthly_cost(months_ago=args.months + 1)
    services = get_cost_by_service(months_ago=args.months)

    print(format_summary(this_month, last_month))
    print("\nBreakdown per Service:")
    print(format_service_table(services, this_month))
    print()


if __name__ == "__main__":
    main()
