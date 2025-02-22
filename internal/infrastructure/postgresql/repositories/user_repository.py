from dataclasses import dataclass

from internal.infrastructure.postgresql.database import Database
from internal.models.identity.user import User


@dataclass
class UserRepository:
    db: Database

    def find_user_by_email(self, email: str) -> User | None:
        query = "select * from t_user where c_email='{}'".format(email)

        with self.db.get_cursor() as cursor:
            row = cursor.fetchone(query)

        if row is None:
            return row

        return User(
            row["id"],
            row["c_name"],
            row["c_surname"],
            row["c_email"],
            row["c_verificated"],
            row["c_password_hash"]
        )
