from datetime import datetime, timedelta


def get_date_n_days_before_today(n_days: int) -> datetime:
    return datetime.today() - timedelta(days=n_days)
