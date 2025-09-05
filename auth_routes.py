from fastapi import APIRouter, status, Depends, HTTPException
from database import Session, engine
import models
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session = Session(bind=engine)

@auth_router.get("/")
async def hello():
    return {"message": "Hello, World!"}


@auth_router.post("/signup", response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # ensures ID and other fields are loaded
    return jsonable_encoder(new_user)


@auth_router.post("/login")
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user is None or not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = Authorize.create_access_token(subject=db_user.id)
    refresh_token = Authorize.create_refresh_token(subject=db_user.id)

    response = {"access": access_token, "refresh": refresh_token}
    return jsonable_encoder(response)
