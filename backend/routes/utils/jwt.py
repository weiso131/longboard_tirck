import jwt
import datetime
from fastapi import HTTPException, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import settings
from exception import *

# 秘鑰和加密算法
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

# Token 有效期設置
ACCESS_TOKEN_EXPIRES_IN = 15  # 分鐘
REFRESH_TOKEN_EXPIRES_IN = 7 * 24 * 60  # 7 天



SECURITY = HTTPBearer(
    scheme_name="JWT",
    description="JWT which get from /auth/login."
)



# 2. 生成訪問與刷新 Token
def generate_tokens(payload):
    """
    生成訪問與刷新 Token
    :param user_id: int, 用戶 ID
    :param username: str, 用戶名
    :return: dict, 包含訪問與刷新 Token
    """
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": access_token,
    }


# 3. 驗證 JWT
def verify_jwt(token: HTTPAuthorizationCredentials = Security(SECURITY)):
    """
    驗證 JWT Token
    :param token: str, JWT Token
    :return: dict, 解碼後的 Payload
    :raises: jwt.ExpiredSignatureError, jwt.InvalidTokenError
    """
    
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        raise TOKEN_INVALID
    
def verify_teacher(token: HTTPAuthorizationCredentials = Security(SECURITY)):
    payload = verify_jwt(token)
    if payload["identity"] == 1:
        raise INSUFFICIENT_PERMISSIONS
    return payload
    
UserDepend = Depends(verify_jwt)
TeacherDepend = Depends(verify_teacher)
