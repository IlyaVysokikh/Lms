from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class ApplicationException(HTTPException):
    @property
    def message(self):
        return "Application Exception occurred"