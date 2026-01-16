from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.jwt import TokenDataSchema, TokenOutSchema
from app.core.database import get_db
from app.models.users import User


#============ OAuth2 scheme =============#
# oauth2_scheme go t find automatically the token in the header with Depends()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
) 



#============ CONSTANTES =============================#
SECRET_KEY = "patate2000"
ALGORITHM = "HS256"
EXPIRE_TOKEN_MINUTES = 30

#========== Error to raise ============#
ERROR_CREDENTIALES = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials...",
    headers={"WWW-Authenticate":"Bearer"}
)


# creation jwt token access
def create_access_token(data:dict)->str:
    to_encode = data.copy()
    # WARNING use .timestamp() for convert datetime into format for jwt:
    now = datetime.now(timezone.utc)
    expiration_time = int((now + timedelta(minutes=EXPIRE_TOKEN_MINUTES)).timestamp())
    created_at = int(now.timestamp())
    to_encode["exp"] = expiration_time
    to_encode["iat"] = created_at

    encoded_token = jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_token


# verification token if not error return user id:
def token_verification(token:str, cred_exception: HTTPException):
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
                             )
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise cred_exception
        return TokenDataSchema(id=user_id)
    except JWTError:
        raise cred_exception

# get current user
def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db))->User:
    token_data = token_verification(token=token, cred_exception=ERROR_CREDENTIALES)
    user = db.query(User).filter(User.id == token_data.id).first()
    if not user:
        raise ERROR_CREDENTIALES
    return user