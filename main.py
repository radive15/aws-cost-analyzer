import logging

from src.cost_explorer import get_monthly_cost

# Setup logging — biasakan ini dari awal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Entry point utama."""
    print("\n=== AWS Cost Analyzer ===\n")

    this_month = get_monthly_cost(months_ago=0)
    last_month = get_monthly_cost(months_ago=1)

    diff = this_month - last_month
    pct = (diff / last_month * 100) if last_month > 0 else 0
    trend = "📈" if diff > 0 else "📉"

    print(f"Bulan ini   : ${this_month:.2f} USD")
    print(f"Bulan lalu  : ${last_month:.2f} USD")
    print(f"Perubahan   : {trend} {diff:+.2f} USD ({pct:+.1f}%)")
    print()


if __name__ == "__main__":
    main()
