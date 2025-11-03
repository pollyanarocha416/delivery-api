import logging
import logging.config
import yaml
from pathlib import Path


def setup_logging():
    config_path = Path(__file__).parent.parent / "logging.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
