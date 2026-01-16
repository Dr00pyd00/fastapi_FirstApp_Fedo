from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.jwt import TokenOutSchema
from app.core.database import get_db
from app.models.users import User
from app.utils.pw_security import verify_pw
from app.utils.jwt import create_access_token


router = APIRouter(
    tags= ["authentication"] 
)

#======= ERROR CREDENTIALES =======#
WRONG_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Wrong credentials!"
)

# WARNING: OAuth2PasswordRequestForm = avec Depends: va chercher le "username" et "password" dans le header

@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=TokenOutSchema)
async def login(user_cred:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db))->TokenOutSchema:
    # check if user exist:
    user = db.query(User).filter(User.username == user_cred.username).first()
    if not user:
        raise WRONG_CREDENTIALS
    # check if password feet with databased pw:
    if not verify_pw(user_cred.password, user.password):
        raise WRONG_CREDENTIALS
    
    token = create_access_token({"sub":user.id})

    return {"access_token":token,
            "token_type":"bearer"}
