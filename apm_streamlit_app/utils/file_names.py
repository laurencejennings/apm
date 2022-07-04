from typing import Union

from apm_streamlit_app.utils.input_manipulation import (
    convert_percentage_to_fraction_string,
)


def create_file_name_from_params(
    prefix: str,
    min_items_value: int,
    confidence_value: int,
    interest_value: Union[str, int],
    node_sizing: str,
) -> str:
    min_conf = convert_percentage_to_fraction_string(confidence_value)
    min_interest = convert_percentage_to_fraction_string(interest_value)
    min_items = str(min_items_value)
    size = str(node_sizing).lower().replace(" ", "_")

    return f"{prefix}__min_items_{min_items}__min_confidence_{min_conf}__min_interest_{min_interest}__node_wt_{size}.html"
