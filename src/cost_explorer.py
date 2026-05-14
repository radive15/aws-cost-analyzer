import logging
from datetime import date, timedelta
from typing import Any

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from src.config import AWS_PROFILE, AWS_REGION

logger = logging.getLogger(__name__)


def _get_client() -> Any:
    """Buat boto3 client untuk Cost Explorer."""
    session = boto3.Session(profile_name=AWS_PROFILE)
    return session.client("ce", region_name=AWS_REGION)


def _get_month_range(months_ago: int = 0) -> tuple[str, str]:
    """
    Hitung start dan end date untuk bulan tertentu.

    months_ago=0 → bulan ini
    months_ago=1 → bulan lalu
    """
    today = date.today()
    # Mundur ke bulan pertama dari bulan target
    first_of_current = today.replace(day=1)
    for _ in range(months_ago):
        first_of_current = (first_of_current - timedelta(days=1)).replace(day=1)

    # End date = hari pertama bulan berikutnya
    if months_ago == 0:
        end = today.strftime("%Y-%m-%d")
    else:
        next_month = (first_of_current.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month.strftime("%Y-%m-%d")

    start = first_of_current.strftime("%Y-%m-%d")
    return start, end


def get_monthly_cost(months_ago: int = 0) -> float:
    """
    Ambil total cost AWS untuk bulan tertentu dalam USD.

    Args:
        months_ago: 0 = bulan ini, 1 = bulan lalu, dst

    Returns:
        Total cost dalam float USD
    """
    start, end = _get_month_range(months_ago)
    logger.info(f"Mengambil cost untuk periode {start} s/d {end}")

    try:
        client = _get_client()
        response = client.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
        )
        amount = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
        return float(amount)

    except NoCredentialsError:
        logger.error("AWS credentials tidak ditemukan. Jalankan 'aws configure' dulu.")
        raise
    except ClientError as e:
        logger.error(f"AWS API error: {e.response['Error']['Message']}")
        raise


def get_cost_by_service(months_ago: int = 0) -> list[dict]:
    """
    Ambil breakdown cost per AWS service.

    Args:
        months_ago: 0 = bulan ini, 1 = bulan lalu, dst

    Returns:
        List of dict {"service": str, "cost": float}, diurutkan dari terbesar
    """
    start, end = _get_month_range(months_ago)
    logger.info(f"Mengambil breakdown per service: {start} s/d {end}")

    try:
        client = _get_client()
        response = client.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )

        results = []
        for group in response["ResultsByTime"][0]["Groups"]:
            service = group["Keys"][0]
            cost = float(group["Metrics"]["UnblendedCost"]["Amount"])
            if cost > 0:
                results.append({"service": service, "cost": cost})

        return sorted(results, key=lambda x: x["cost"], reverse=True)

    except NoCredentialsError:
        logger.error("AWS credentials tidak ditemukan.")
        raise
    except ClientError as e:
        logger.error(f"AWS API error: {e.response['Error']['Message']}")
        raise
