from dataclasses import dataclass
from datetime import datetime

from internal.infrastructure.postgresql.database import Database


@dataclass
class TokenRepository:
    db: Database

    def save(
            self,
            refresh_token: str,
            expires_at: datetime,
            user_oid: int,
            active
             ) -> None:
        query = "insert into t_user_token (c_token, c_expires_at, c_active, id_user) values (%s, %s, %s, %s)"

        with self.db.get_cursor() as cursor:
            cursor.execute(query, (refresh_token, expires_at, active, user_oid))