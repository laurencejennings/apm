from apm_streamlit_app.utils.input_manipulation import (
    convert_percentage_to_fraction_string,
)


class TestInputManipulation:
    def test_convert_percentage_to_fraction_string(self):
        actual = convert_percentage_to_fraction_string(47)
        assert actual == "0_47"

    def test_convert_percentage_to_fraction_string__nothreshold(self):
        actual = convert_percentage_to_fraction_string("No threshold")
        assert actual == "-1_0"

    def test_convert_percentage_to_fraction_string__100(self):
        actual = convert_percentage_to_fraction_string(100)
        assert actual == "1_0"
