from __future__ import annotations

from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from jose.jwt import decode
from jwt import exceptions

from jose import jwt, ExpiredSignatureError
from jwt.api_jwt import encode
from jwt.jwks_client import PyJWKClient

from crud.CompanyCRUD import company_crud
from models import models
from schemas import user_schemas
from services.hasher import Hasher
from utils.config import settings
from crud.UserCRUD import user_crud

token_auth_scheme = HTTPBearer()


class Auth:
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = encode(payload=to_encode, key=settings.secret_key,
                             algorithm=settings.algorithm)
        return encoded_jwt

    async def authenticate_user(username: str, password: str):
        user = await user_crud.get_by_username(username=username)
        if not user:
            return False
        if not Hasher.verify_password(plain_password=password, hashed_password=user.hashed_password):
            return False
        return user

    @staticmethod
    def decode_access_token(token):
        try:
            decoded = jwt.decode(token.credentials, settings.secret_key, algorithms=settings.algorithm)
        except ExpiredSignatureError:
            raise HTTPException(detail="Signature has expired, you should recreate access token", status_code=404)
        return decoded

    async def get_current_user(token: str = Depends(token_auth_scheme)):
        if not jwt.get_unverified_header(token.credentials) == {"alg": "RS256", "typ": "JWT"}:
            result = VerifyToken(token.credentials).verify()
            user = await user_crud.get_by_email(result[".email"])
            if not user:
                user = user_schemas.User(email=result[".email"], username=result[".email"],
                                         hashed_password=token.credentials[::-1][:10], is_active=False)
                await user_crud.add(user)
                return user
        else:
            result = Auth().decode_access_token(token)
        user = await user_crud.get_by_email(result[".email"])
        return user

    async def get_role(user_id: int, company_id: int):
        company = await company_crud.get_company(company_id)
        user = await user_crud.get_user(user_id)
        if user.company_id is None:
            return 0  # user
        if company.id != user.company_id:
            return -1
        if company.owner_id == user_id:
            return 3  # owner
        admins = await company_crud.get_admins(company.id)
        for admin in admins:
            if admin.user_id == user_id:
                return 2  # admin
        members = await company_crud.get_members(company.id)
        for member in members:
            if member.id == user_id:
                return 1  # member



class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self, token):
        self.token = token

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{settings.domain}/.well-known/jwks.json'
        self.jwks_client = PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = decode(
                self.token,
                self.signing_key,
                algorithms=settings.algorithms,
                audience=settings.api_audience,
                issuer=settings.issuer
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload
