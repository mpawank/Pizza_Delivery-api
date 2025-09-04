from pydantic import BaseModel
from typing import Optional

from sqlalchemy import false, true

class SignUpModel(BaseModel):
  id: Optional[int]
  username: str
  email: str
  password: str
  is_staff: Optional[bool]
  is_active: Optional[bool]


  class Config:
    orm_mode = True
    schema_extra = {
      "example": {
        "username": "john_doe",
        "email": "john_doe@example.com",
        "password": "securepassword",
        "is_staff": false,
        "is_active": true
      }
    }
