from apm_streamlit_app.utils.file_names import create_file_name_from_params


class TestFileNames:
    def test_create_file_name_from_params(self):
        actual = create_file_name_from_params("prefix", "1", "2", "3", "4")
        assert (
            actual
            == "prefix__min_items_1__min_confidence_2__min_interest_3__node_wt_4.html"
        )
