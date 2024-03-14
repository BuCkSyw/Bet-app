from typing import Literal

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class LiteralProviderSettings(BaseSettings):

    MODE: Literal["TEST", "DEV"]

    DB_HOST_PROV: str
    DB_PORT_PROV: int
    DB_USER_PROV: str
    DB_PASS_PROV: str
    DB_NAME_PROV: str

    @property
    def PROV_DATABASE_URL(self) -> AnyHttpUrl:
        return f"postgresql+asyncpg://{self.DB_USER_PROV}:{self.DB_PASS_PROV}@{self.DB_HOST_PROV}:{self.DB_PORT_PROV}/{self.DB_NAME_PROV}"

    TEST_DB_HOST_PROV: str
    TEST_DB_PORT_PROV: int
    TEST_DB_USER_PROV: str
    TEST_DB_PASS_PROV: str
    TEST_DB_NAME_PROV: str

    @property
    def PROV_TEST_DATABASE_URL(self) -> AnyHttpUrl:
        return f"postgresql+asyncpg://{self.TEST_DB_USER_PROV}:{self.TEST_DB_PASS_PROV}@{self.TEST_DB_HOST_PROV}:{self.TEST_DB_PORT_PROV}/{self.TEST_DB_NAME_PROV}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


provider_settings = LiteralProviderSettings()
