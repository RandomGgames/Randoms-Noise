import logging
import pathlib
import sys
import time
import toml
import traceback
import typing
from datetime import datetime

logger = logging.getLogger(__name__)

"""
Python Script Template
"""


def load_config(config_path: str = "config.toml") -> dict:
    logger.debug("Loading config...")
    config = toml.load(config_path)

    logger.debug("Validating config...")
    required_keys = {
        "assets_dir": str,
        "file_extensions": list
    }
    for key, expected_type in required_keys.items():
        if key not in config or not isinstance(config[key], expected_type):
            raise ValueError(
                f"config.toml is missing or has incorrect type for key '{key}' (expected {expected_type.__name__})")
    if not all(key in config for key in required_keys):
        raise ValueError(
            f"config.toml is missing required key(s): {', '.join(sorted(list(set(required_keys) - set(config.keys()))))}")
    logger.debug("Config loaded successfully.")
    return config


def get_texture_file_paths(config: dict) -> typing.Iterable[pathlib.Path]:
    assets_dir = pathlib.Path(config["assets_dir"]).resolve()
    logger.debug(f"Searching for media files in '{assets_dir}'...")
    for file_path in assets_dir.rglob("*"):
        if file_path.is_file():
            if file_path.suffix[1:] in config["file_extensions"]:
                logger.debug(f"Found media file: {file_path}")
                yield file_path


def main() -> None:
    config_path = "build_noise_textures.toml"
    config = load_config(config_path)
    texture_file_paths = get_texture_file_paths(config)

    for file_path in texture_file_paths:
        logger.debug(f"Processing media file: {file_path}")


def setup_logging(
        logger: logging.Logger,
        log_file_path: typing.Union[str, pathlib.Path],
        console_logging_level: int = logging.DEBUG,
        file_logging_level: int = logging.DEBUG,
        log_message_format: str = "%(asctime)s.%(msecs)03d %(levelname)s [%(funcName)s] [%(name)s]: %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S") -> None:
    logger.setLevel(file_logging_level)  # Set the overall logging level

    # File Handler for script-named log file (overwrite each run)
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8", mode="w")
    file_handler.setLevel(file_logging_level)
    file_handler.setFormatter(logging.Formatter(log_message_format, datefmt=date_format))
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_logging_level)
    console_handler.setFormatter(logging.Formatter(log_message_format, datefmt=date_format))
    logger.addHandler(console_handler)

    # Set specific logging levels if needed
    # logging.getLogger("requests").setLevel(logging.INFO)


if __name__ == "__main__":
    script_name = pathlib.Path(__file__).stem
    log_file_name = f"{script_name}.log"
    log_file_path = pathlib.Path(log_file_name)
    setup_logging(logger, log_file_path, log_message_format="%(asctime)s.%(msecs)03d %(levelname)s [%(funcName)s]: %(message)s")

    error = 0
    try:
        start_time = time.perf_counter()
        logger.info("Starting operation...")
        main()
        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"Completed operation in {duration:.4f}s.")
    except Exception as e:
        logger.warning(f"A fatal error has occurred: {repr(e)}\n{traceback.format_exc()}")
        error = 1
    finally:
        sys.exit(error)
