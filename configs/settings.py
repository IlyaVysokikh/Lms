from pydantic import RedisDsn, AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str

    REDIS_URL: RedisDsn

    PISTON_URL: AnyUrl

    SECRET_KEY: str
    ALGORITHM : str
    ACCESS_TOKEN_TTL: int
    REFRESH_TOKEN_TTL: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def build_pg_dns(self) -> str:
        return (f"postgresql://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:5432/{self.POSTGRES_DB}")

