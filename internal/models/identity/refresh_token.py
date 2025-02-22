from dataclasses import dataclass
from datetime import datetime


@dataclass
class RefreshToken:
    oid: int
    token: str
    expires_at: datetime
    active: bool
    user_oid: int