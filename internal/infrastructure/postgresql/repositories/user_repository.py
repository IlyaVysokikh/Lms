from dataclasses import dataclass

from internal.infrastructure.postgresql.database import Database
from internal.models.identity.user import User


@dataclass
class UserRepository:
    db: Database

    def find_user_by_email(self, email: str) -> User | None:
        query = "select * from t_user where c_email='{}'".format(email)

        with self.db.get_cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

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

    def save_user(self, name: str, surname: str, email: str, hashed_password: bytes) -> bool:
        query = "insert into t_user (c_name, c_surname, c_email, c_password_hash, c_verificated) values (%s, %s, %s, %s, %s)"

        with self.db.get_cursor() as cursor:
            cursor.execute(query, (name, surname, email, hashed_password, False))

            if cursor.rowcount == 1:
                cursor.connection.commit()
                return True

            cursor.connection.rollback()

        return False

    def verify_user(self, email: str) -> bool:
        query = "update t_user set c_verificated=true where c_email='{}'".format(email)

        with self.db.get_cursor() as cursor:
            cursor.execute(query)
