from dataclasses import dataclass


@dataclass
class User:
    oid: int
    name: str
    surname: str
    email: str
    verified: bool
    password_hash: str
