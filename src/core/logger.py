"""Custom logger."""

from sys import stdout
from typing import Set

import loguru
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggerSettings(BaseSettings):

    levels: Set[str] = {"DEBUG", "INFO", "WARNING", "ERROR"}

    model_config = SettingsConfigDict(env_prefix="logger_")


def create_logger(levels: Set[str]):  # type: ignore
    """Create custom logger."""
    loguru.logger.remove()
    for level in levels:
        loguru.logger.add(
            stdout,
            colorize=True,
            level=level,
            catch=True,
        )

    loguru.logger.add("loguru.log")
    return loguru.logger


logger_settings = LoggerSettings()
logger = create_logger(logger_settings.levels)
