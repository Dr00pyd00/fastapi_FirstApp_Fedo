from pydantic import BaseModel
from datetime import datetime


#====== POSTS SCHEMAS ============#

class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateSchema(PostBaseSchema):
    pass 

class PostUpdateSchema(PostBaseSchema):
    pass 

# When DB send data about a post:
class PostResponseSchema(PostBaseSchema):
    id: int
    created_at: datetime

    # because come from DB ORM:
    model_config = {"from_attributes":True}