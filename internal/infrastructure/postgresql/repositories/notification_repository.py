from dataclasses import dataclass

from internal.infrastructure.postgresql.database import Database
from internal.models.social.notification_template import NotificationTemplate

@dataclass
class NotificationRepository:
    database: Database

    def get_notification_by_type(self, notification_type: str) -> NotificationTemplate | None:
        query = "select * from t_notification where c_type = '{}'".format(notification_type)

        with self.database.get_cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

            if row is None:
                return None

            return NotificationTemplate(
                body=row["c_text"],
                notification_type=notification_type
            )