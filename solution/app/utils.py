import json
import base64

from math import floor
from binascii import crc32
from datetime import datetime
from typing import Tuple, Optional

from fastapi import Request, Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from app.models.user import User
from app.exceptions import APIError
from app.repositories.user import UserRepository, get_user_repository

TOKEN_SEPARATOR = ";"
TOKEN_LIFETIME = 60 * 60  # 1 hour


def authenticate_user_token(
    request: Request,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    user_repository: UserRepository = Depends(get_user_repository)
) -> User:
    if hasattr(request.state, "user"):
        return request.state.user
    elif auth is None:
        raise APIError(
            status_code=401,
            reason="Переданный токен не существует либо некорректен."
        )
    
    login, timestamp, password = parse_token(auth.credentials)
    current_timestamp = datetime.utcnow().timestamp()
    
    if login is None or (current_timestamp - timestamp) > TOKEN_LIFETIME:
        raise APIError(
            status_code=401,
            reason="Переданный токен не существует либо некорректен."
        )
    
    user = user_repository.find_by_password(login=login, password=password)
    if user is None:
        raise APIError(
            status_code=401,
            reason="Переданный токен не существует либо некорректен."
        )
    
    request.state.user = user
    return user


def generate_token(login: str, password: str) -> str:
    data = json.dumps({
        "login": login,
        "password": password,
        "timestamp": "{:.0f}".format(datetime.utcnow().timestamp())
    })
    
    return "$$$" + base64.b64encode(data.encode("utf-8")).decode("utf-8")


def parse_token(token: str) -> Optional[Tuple[str, int, str]]:
    if not token.startswith("$$$"):
        return None, -1, None
    
    content = base64.b64decode(token[3:].encode("utf-8")).decode("utf-8")
    data = json.loads(content)
    
    return data["login"], int(data["timestamp"]), data["password"]


"""
def generate_token(login: str, password: str) -> str:
    # token format: login:str, timestamp:int, password:str
    data = TOKEN_SEPARATOR.join([login, "{:.0f}".format(datetime.utcnow().timestamp()), password])
    return data + TOKEN_SEPARATOR + hex(crc32(data.encode("utf-8")))[2:]


def parse_token(token: str) -> Optional[Tuple[str, int, str]]:
    # 1st: x;x;x;yyyyyyyy
    if len(token) < 14 or token.count(TOKEN_SEPARATOR) < 3:
        return None, -1, None
    
    parts = token.split(TOKEN_SEPARATOR)
    data = TOKEN_SEPARATOR.join(parts[:-1])
    hashsum = parts[-1]
    
    # 2nd: check hashsum at the end
    if len(hashsum) != 8 or hex(crc32(data.encode("utf-8")))[2:] != hashsum:
        return None, -1, None
    
    return parts[0], int(parts[1]), TOKEN_SEPARATOR.join(parts[2:-1])
"""
