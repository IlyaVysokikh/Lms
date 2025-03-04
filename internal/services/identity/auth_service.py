from dataclasses import dataclass
from datetime import datetime, timedelta

import bcrypt
import jwt

from configs.settings import AuthSettings
from internal.handlers.identity.schema.token_pair_schema import TokenPairSchema
from internal.infrastructure.postgresql.repositories.token_repository import TokenRepository


@dataclass
class AuthService:
    token_repository: TokenRepository
    settings: AuthSettings

    def verify_password(self, plain_password: str, hashed_password) -> bool:
        plain_password_bytes = plain_password.encode("utf-8")
        hashed_password_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

    def create_tokens_pair(self, user_oid: int, email: str) -> TokenPairSchema:
        access_token = self.__create_access_token__(user_oid, email)
        refresh_token = self.create_refresh_token(user_oid, email)

        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)

    def create_refresh_token(self, user_oid: int, email: str) -> str:
        expires = datetime.utcnow() + timedelta(days=self.settings.REFRESH_TOKEN_TTL)
        payload = {
            "user_oid": user_oid,
            "email": email,
            "type": "refresh",
            "exp": expires
        }
        token = jwt.encode(payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)

        self.save_refresh_token(token, expires, user_oid)

        return token

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Токен истёк")
        except jwt.InvalidTokenError:
            raise ValueError("Недействительный токен")

    def save_refresh_token(
            self,
            refresh_token: str,
            expires_at: datetime,
            user_oid: int,
            active: bool = True
    ) -> None:
        self.token_repository.save(refresh_token, expires_at, user_oid, active)

    def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def __create_access_token__(self, user_oid: int, email: str) -> str:
        payload = {
            "user_oid": user_oid,
            "email": email,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=self.settings.ACCESS_TOKEN_TTL)
        }
        token = jwt.encode(payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)

        return token

