from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.users import UserCreateSchema, UserResponseSchema
from app.core.database import get_db
from app.utils.pw_security import hash_pw, verify_pw


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# WARNING: problem bcrypt:
# pip uninstall bcrypt passlib -y
# pip install passlib[bcrypt] bcrypt==4.0.1

#=========== USER CRUD ==============#

# create new user:
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
async def create_user(user_data:UserCreateSchema, db:Session=Depends(get_db)):
    # check if user already exist:
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username already taken!"
        )    
    user_dict = user_data.model_dump()
    # hash the pw for DB:
    hashed_pw = hash_pw(user_data.password)
    user_dict["password"] = hashed_pw
    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# retrieve user by ID:
@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def detail_user_by_id(id:int, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with ID:{id} NOT FOUND!"
        )
    return user