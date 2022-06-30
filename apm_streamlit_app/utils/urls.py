from datetime import datetime, timedelta
from typing import Any, Dict, List

import requests  # type: ignore


def generate_url(graph_date: datetime, fname: str, config: Dict[str, Any]):
    failed_dates: List[datetime] = []
    errors: List[datetime] = []
    for index in range(0, 6):
        cur_date = graph_date - timedelta(days=index)
        url = f"{config.get('paths')['s3_base_url']}/{cur_date.strftime('%Y-%m-%d')}/{fname}"
        if requests.head(url).status_code == 200:
            return (url, cur_date, failed_dates)
        else:
            failed_dates.append(cur_date)
        for failed_date in failed_dates:
            errors.append(failed_date)
    return (None, None, errors)
