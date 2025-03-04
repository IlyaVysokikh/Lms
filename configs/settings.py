from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="configs/.env")

class PostgresSettings(BaseModel):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str

    def build_pg_dns(self) -> str:
        return (f"postgresql://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:5432/{self.POSTGRES_DB}")

class AuthSettings(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_TTL: int
    REFRESH_TOKEN_TTL: int

class SMTPSettings(BaseModel):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

class Settings(BaseSettings):
    postgres_settings: PostgresSettings = PostgresSettings(
        POSTGRES_USER=os.getenv("POSTGRES_USER"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
        POSTGRES_SERVER=os.getenv("POSTGRES_SERVER"),
        POSTGRES_DB=os.getenv("POSTGRES_DB"),
    )
    redis_url: str = os.getenv("REDIS_URL")
    piston_url: str = os.getenv("PISTON_URL")
    auth_settings: AuthSettings = AuthSettings(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        ALGORITHM=os.getenv("ALGORITHM"),
        ACCESS_TOKEN_TTL=int(os.getenv("ACCESS_TOKEN_TTL", 3600)),
        REFRESH_TOKEN_TTL=int(os.getenv("REFRESH_TOKEN_TTL", 86400)),
    )
    smtp_settings: SMTPSettings = SMTPSettings(
        SMTP_HOST=os.getenv("SMTP_HOST"),
        SMTP_PORT=int(os.getenv("SMTP_PORT", 465)),
        SMTP_USER=os.getenv("SMTP_USER"),
        SMTP_PASSWORD=os.getenv("SMTP_PASSWORD"),
    )
