from typing import Literal

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class BetMakerSettings(BaseSettings):
    MODE: Literal["TEST", "DEV"]

    DB_HOST_BET: str
    DB_PORT_BET: int
    DB_USER_BET: str
    DB_PASS_BET: str
    DB_NAME_BET: str

    @property
    def BET_DATABASE_URL(self) -> AnyHttpUrl:
        return f"postgresql+asyncpg://{self.DB_USER_BET}:{self.DB_PASS_BET}@{self.DB_HOST_BET}:{self.DB_PORT_BET}/{self.DB_NAME_BET}"

    TEST_DB_HOST_BET: str
    TEST_DB_PORT_BET: int
    TEST_DB_USER_BET: str
    TEST_DB_PASS_BET: str
    TEST_DB_NAME_BET: str

    @property
    def BET_TEST_DATABASE_URL(self) -> AnyHttpUrl:
        return f"postgresql+asyncpg://{self.TEST_DB_USER_BET}:{self.TEST_DB_PASS_BET}@{self.TEST_DB_HOST_BET}:{self.TEST_DB_PORT_BET}/{self.TEST_DB_NAME_BET}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


bet_settings = BetMakerSettings()
