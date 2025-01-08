import logging

import yaml

from config.paths import SUBLAYERS_CONFIG_PATH
from karapyner.builders import ConfigurationError
from karapyner.karabiner import KarabinerConfig

logger = logging.getLogger(__name__)


def load_config(config_path: str = SUBLAYERS_CONFIG_PATH) -> dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        raise


def create_config():
    """Create and save Karabiner configuration"""
    try:
        config = load_config()
        kb = KarabinerConfig()
        kb.create_config_from_dict(config)
        kb.save_config()
        logger.info("Configuration created and saved successfully")
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    try:
        create_config()
    except Exception as e:
        logger.error(f"Failed to create configuration: {e}")
        exit(1)
