import jwt

from fastapi import Header, Security
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader

from src.archive.config import SECRET_KEY, ALGORITHM
from src.archive.domains.user import Role


def decode_jwt_token(authorization_header: str):
    if authorization_header is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if "Bearer" not in authorization_header:
        raise HTTPException(status_code=401, detail="Authorization error")
    
    clear_token = authorization_header.replace("Bearer ", "")
    try:
        data = jwt.decode(clear_token, SECRET_KEY, ALGORITHM)
        return data
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Authorization error")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Authorization error")

def check_access_token(authorization_header: str = Security(APIKeyHeader(name="Authorization", auto_error=False))):
    return decode_jwt_token(authorization_header)

def check_role(authorization_header: str = Security(APIKeyHeader(name="Authorization", auto_error=False))):
    data = decode_jwt_token(authorization_header)
    
    required_roles = [Role.AdminUser.value, Role.RedactorUser.value]
    
    if data["role"] not in required_roles:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return data


def check_all_admin_group_role(authorization_header: str = Security(APIKeyHeader(name="Authorization", auto_error=False))):
    data = decode_jwt_token(authorization_header)
    required_roles = [Role.AdminUser.value, Role.RedactorUser.value, Role.ScientificCouncil.value]
    
    if data["role"] not in required_roles:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return data


def check_sci_role(authorization_header: str = Security(APIKeyHeader(name="Authorization", auto_error=False))):
    data = decode_jwt_token(authorization_header)
    required_roles = [Role.ScientificCouncil.value]
    
    if data["role"] not in required_roles:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return data


def check_super_admin_role(authorization_header: str = Security(APIKeyHeader(name="Authorization", auto_error=False))):
    data = decode_jwt_token(authorization_header)
    required_roles = [Role.SuperAdminUser.value]

    if data["role"] not in required_roles:
        raise HTTPException(status_code=403, detail="Access denied")

    return data

