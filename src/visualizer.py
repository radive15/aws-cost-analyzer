import logging
from pathlib import Path
import matplotlib.pyplot as plt

from src.utils import get_period_label

logger = logging.getLogger(__name__)


def save_chart(
    services: list[dict],
    total_usd: float,
    rate: float,
    months_ago: int = 0,
    output_dir: str = ".",
) -> str:
    """
    Buat horizontal bar chart breakdown cost per service dan simpan ke PNG.

    Args:
        services: List of {"service": str, "cost": float}, sudah diurutkan dari terbesar
        total_usd: Total cost dalam USD (untuk label judul)
        rate: Exchange rate USD ke IDR
        months_ago: 0 = bulan ini, 1 = bulan lalu
        output_dir: Folder tujuan file PNG

    Returns:
        Path lengkap file PNG yang dibuat
    """
    if not services:
        logger.warning("Tidak ada data service untuk divisualisasikan.")
        raise ValueError("Data service kosong")

    period = get_period_label(months_ago)
    filename = Path(output_dir) / f"aws-cost-{period}.png"

    # Pisahkan nama service dan nilai cost — matplotlib butuh 2 list terpisah
    names = [s["service"] for s in services]
    costs = [s["cost"] for s in services]

    # Balik urutan supaya bar terbesar tampil di atas (matplotlib menggambar dari bawah)
    names = names[::-1]
    costs = costs[::-1]

    fig, ax = plt.subplots(figsize=(10, max(4, len(names) * 0.5)))

    bars = ax.barh(names, costs, color="#FF9900", edgecolor="white")

    # Label nilai USD di ujung tiap bar
    for bar, cost in zip(bars, costs):
        ax.text(
            bar.get_width() + total_usd * 0.005,  # sedikit geser ke kanan
            bar.get_y() + bar.get_height() / 2,
            f"${cost:.2f}",
            va="center",
            fontsize=8,
        )

    ax.set_xlabel("Cost (USD)")
    ax.set_title(f"AWS Cost by Service — {period}\nTotal: ${total_usd:.2f} USD  |  Rp {total_usd * rate:,.0f}")
    ax.set_xlim(0, max(costs) * 1.2)  # kasih ruang untuk label di kanan
    plt.tight_layout()

    try:
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close(fig)  # tutup figure supaya tidak makan memory
        logger.info(f"Chart disimpan: {filename}")
        return str(filename)
    except OSError as e:
        logger.error(f"Gagal menyimpan chart ke {filename}: {e}")
        raise
