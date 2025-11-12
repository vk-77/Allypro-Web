"""
Centralized test data — migrated from Cypress dataload.js.

Provides account credentials, supervisor credentials, and dynamic date helpers.
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from config.web_settings import (
    BASE_URL,
    COMPANY,
    USERNAME,
    PASSWORD,
    SUPERVISOR_COMPANY,
    SUPERVISOR_USERNAME,
    SUPERVISOR_PASSWORD,
)


def _fmt(dt, fmt):
    return dt.strftime(fmt)


_now = datetime.now()

account = {
    "company": COMPANY,
    "username": USERNAME,
    "password": PASSWORD,
    "base_url": BASE_URL,
    "url_after_valid_login": "**/Home/GetToastAlertPartial",
}

supervisor = {
    "company": SUPERVISOR_COMPANY,
    "username": SUPERVISOR_USERNAME,
    "password": SUPERVISOR_PASSWORD,
}

dates = {
    "today": _fmt(_now, "%m/%d/%Y"),
    "d5_days_ago": _fmt(_now - timedelta(days=5), "%m/%d/%Y"),
    "one_month_ago": _fmt(_now - relativedelta(months=1), "%m/%d/%Y"),
    "today_dash": _fmt(_now, "%m-%d-%Y"),
    "today_api_format": _fmt(
        _now + timedelta(days=1), "%Y-%m-%dT%H:%M:%S.200"
    ),
    "next_year": _fmt(_now + relativedelta(years=1), "%Y"),
    "five_months_earlier_first_of_month": _fmt(
        (_now - relativedelta(months=5)).replace(day=1), "%m/%d/%Y"
    ),
    "four_months_earlier_end_of_month": _fmt(
        (_now - relativedelta(months=3)).replace(day=1) - timedelta(days=1),
        "%m/%d/%Y",
    ),
    "four_months_earlier_statement_date": _fmt(
        _now - relativedelta(months=4), "%Y-%m-%d"
    ),
    "five_months_earlier": _fmt(_now - relativedelta(months=5), "%m/%d/%Y"),
    "last_month": "12",
    "next_month": _fmt(_now + relativedelta(months=1), "%m/%d/%Y"),
}
