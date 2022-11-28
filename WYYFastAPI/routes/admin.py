from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext
from starlette.status import HTTP_200_OK

from auth.jwt_handler import sign_jwt
from database.database import add_admin
from models.admin import Admin, AdminData, AdminSignIn

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def admin_login(admin_credentials: AdminSignIn = Body(...)):
    admin_exists = await Admin.find_one(Admin.email == admin_credentials.username)
    if admin_exists:
        password = hash_helper.verify(
            admin_credentials.password, admin_exists.password
        )
        if password:
            return sign_jwt(admin_credentials.username)

        raise HTTPException(
            status_code=403,
            detail="Incorrect email or password"
        )

    raise HTTPException(
        status_code=403,
        detail="Incorrect email or password"
    )


@router.post(path="/new", response_model=AdminData, summary='sign up')
async def admin_signup(req_body: Admin = Body(...)):
    admin_exists = await Admin.find_one(Admin.email == req_body.email)
    if admin_exists:
        raise HTTPException(
            status_code=409,
            detail="Admin with email supplied already exists"
        )

    req_body.password = hash_helper.encrypt(req_body.password)
    await add_admin(req_body)
    return {'status_code': HTTP_200_OK, 'msg': 'success'}

