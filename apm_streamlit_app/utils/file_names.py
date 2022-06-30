def create_file_name_from_params(
        prefix: str,
        min_items: str,
        min_conf: str,
        min_interest: str,
        size: str) -> str:
    return f"{prefix}__min_items_{min_items}__min_confidence_{min_conf}__min_interest_{min_interest}__node_wt_{size}.html"
