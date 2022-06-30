import os
from pathlib import Path

import yaml  # type: ignore

ROOT_PATH = os.path.dirname(os.path.dirname(Path(__file__)))
CONFIG_PATH = os.path.join(ROOT_PATH, 'resources', 'config.yaml')

def read_config_from_path(config_file_path: str):  # pragma: no cover
    with open(config_file_path, "r") as fp:
        config = yaml.load(fp, Loader=yaml.FullLoader)

        return config
