from dataclasses import dataclass


@dataclass
class NotificationTemplate:
    notification_type: str
    body: str