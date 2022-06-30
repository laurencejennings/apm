from datetime import datetime, timedelta

from apm_streamlit_app.utils.dates import get_date_n_days_before_today


class TestDates:
    def test_get_date_n_days_before_today(self):
        actual = get_date_n_days_before_today(4)
        assert actual.date() == (datetime.today() - timedelta(days=4)).date()
