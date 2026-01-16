from pydantic import BaseModel
from datetime import datetime



#========= USERS schemas =========#

class UserBaseSchema(BaseModel):
    username: str

class UserFullDataSchema(UserBaseSchema):
    id: int
    created_at: datetime
    password: str 

class UserResponseSchema(UserBaseSchema):
    id: int
    created_at: datetime

    model_config = {"from_attributes":True}

class UserCreateSchema(UserBaseSchema):
    password: str
