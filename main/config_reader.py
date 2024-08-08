from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
    token_ya: SecretStr
    token_whatsapp: SecretStr
    id_instance: SecretStr


config = Settings()
