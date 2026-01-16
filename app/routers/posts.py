from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List

from app.core.database import get_db
from app.schemas.posts import PostResponseSchema, PostCreateSchema, PostUpdateSchema
from app.models.posts import Post


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#======= ERROR HANDLER =======#
def handler_post_not_found(id:int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"posts with ID: {id} NOT FOUND"
)

#========== CRUD =============#
#=============================#


# all posts:
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponseSchema] | dict)
async def get_all_posts(db:Session=Depends(get_db)):
    posts = db.query(Post).all()
    if not posts:
        return {"message":"no data for now!"}
    return posts

# retrieve one post by ID:
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def detail_post_by_id(id:int, db:Session=Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise handler_post_not_found(id=id)
    return post

# create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
async def create_post(user_data:PostCreateSchema, db:Session=Depends(get_db)):
    data_dict = user_data.model_dump()
    new_post = Post(**data_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# delete a post by ID:
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id:int, db:Session=Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise handler_post_not_found(id=id)
    db.delete(post)
    db.commit()
    return

# update post by ID:
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def update_post_by_id(id:int, up_post_data:PostUpdateSchema, db:Session=Depends(get_db)):
    post_to_up = db.query(Post).filter(Post.id == id).first()
    if not post_to_up:
        raise handler_post_not_found(id=id)
    for k,v in up_post_data.model_dump().items():
        setattr(post_to_up,k,v)
    db.commit()
    db.refresh(post_to_up)
    return post_to_up