from typing import Optional, Any

from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class Admin(Document):
    fullname: str
    email: EmailStr
    password: str

    class Collection:
        name = "admin"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "name",
                "email": "user@example.com",
                "password": "psw"
            }
        }


class AdminSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {
                "username": "abdul@youngest.dev",
                "password": "3xt3m#"
            }
        }


class AdminData(BaseModel):
    status_code: int
    msg: str

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": 'success',
            }
        }
