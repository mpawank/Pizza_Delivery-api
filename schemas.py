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


class Settings(BaseModel):
  authjwt_secret_key: str='6d51da3037ef59491c917fbb7c17dcc9aa3883edb4c075053b3698645fb4ec97'



class LoginModel(BaseModel):
  username: str
  password: str

  