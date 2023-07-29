from __future__ import annotations

from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import HTTPBearer

from jose.jwt import decode
from jwt import exceptions

from jose import jwt
from jwt.api_jwt import encode
from jwt.jwks_client import PyJWKClient

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
        print(to_encode, settings.secret_key, settings.algorithm)
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
        decoded = jwt.decode(token.credentials, settings.secret_key, algorithms=settings.algorithm)
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
