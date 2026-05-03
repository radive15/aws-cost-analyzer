import logging

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

FALLBACK_RATE = 16_500.0


def get_usd_to_idr() -> float:
    """
    Ambil exchange rate USD ke IDR dari frankfurter.app.

    Returns:
        Rate konversi (misal: 16350.0 artinya 1 USD = Rp 16.350)
    """
    try:
        response = requests.get(
            "https://api.frankfurter.app/latest",
            params={"from": "USD", "to": "IDR"},
            timeout=5,
        )
        response.raise_for_status()
        rate = float(response.json()["rates"]["IDR"])
        logger.info(f"Exchange rate: 1 USD = Rp {rate:,.0f}")
        return rate

    except RequestException as e:
        logger.warning(f"Gagal ambil exchange rate: {e}. Pakai fallback Rp {FALLBACK_RATE:,.0f}")
        return FALLBACK_RATE
