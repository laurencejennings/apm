from typing import Union


def convert_percentage_to_fraction_string(value: Union[int, str]) -> str:
    if value == "No threshold":
        return "-1_0"
    if type(value) == int:
        return str(value / 100).replace(".", "_")
    return "False"
