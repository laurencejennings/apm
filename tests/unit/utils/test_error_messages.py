from datetime import datetime

from apm_streamlit_app.utils.error_messages import failed_to_load_graph


class TestErrorMessages:
    def test_failed_to_load_graph(self):
        actual = failed_to_load_graph(datetime(2022, 5, 1))
        assert actual == "Failed to load graph for date: 2022-05-01"
