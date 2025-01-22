import jwt
import datetime
from fastapi import HTTPException, Depends
from config import settings

# 秘鑰和加密算法
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

# Token 有效期設置
ACCESS_TOKEN_EXPIRES_IN = 15  # 分鐘
REFRESH_TOKEN_EXPIRES_IN = 7 * 24 * 60  # 7 天

TOKEN_EXPIRED = HTTPException(status_code=400, detail="token expired")
TOKEN_INVALID = HTTPException(status_code=400, detail="token invalid")




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
def verify_jwt(token):
    """
    驗證 JWT Token
    :param token: str, JWT Token
    :return: dict, 解碼後的 Payload
    :raises: jwt.ExpiredSignatureError, jwt.InvalidTokenError
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        raise TOKEN_INVALID
    
UserDepend = Depends(verify_jwt)
