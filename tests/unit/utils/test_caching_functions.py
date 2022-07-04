import os
from datetime import datetime

from apm_streamlit_app.config.config_loader import ROOT_PATH, read_config_from_path
from apm_streamlit_app.utils.kpe_utils import read_kpe_pickle

config = read_config_from_path(
    os.path.join(os.path.dirname(ROOT_PATH), "tests/resources/test_config.yaml")
)


class TestCachingFunctions:
    def test_read_kpe_pickle(self):
        actual = read_kpe_pickle(datetime(2022, 6, 29), config)
        assert len(actual.keys()) == 505
