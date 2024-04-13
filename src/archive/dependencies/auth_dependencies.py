import jwt

from fastapi import Header, Security
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader

from src.archive.config import SECRET_KEY, ALGORITHM
from src.archive.domains.user import Role


def chech_access_token(authorization_header: str = Security(APIKeyHeader(name="Authorization", auto_error=False))):
    if authorization_header is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if "Bearer" not in authorization_header:
        raise HTTPException(status_code=401, detail="Authorization error")
    
    clear_token = authorization_header.replace("Bearer ", "")
    try:
        data = jwt.decode(clear_token, SECRET_KEY, ALGORITHM)
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Authorization error")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Authorization error")
    
    return data


def chech_role(authorization_header: str = Security(APIKeyHeader(name="Authorization", auto_error=False))):
    if authorization_header is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if "Bearer" not in authorization_header:
        raise HTTPException(status_code=401, detail="Authorization error")
    
    clear_token = authorization_header.replace("Bearer ", "")
    try:
        data = jwt.decode(clear_token, SECRET_KEY, ALGORITHM)
        if data["role"] == Role.AdminUser.value or data["role"] == Role.RedactorUser.value:
            return data
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Authorization error")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Authorization error")
    
    raise HTTPException(status_code=403, detail="Access denied")