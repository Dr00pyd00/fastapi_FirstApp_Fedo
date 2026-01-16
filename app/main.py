from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.posts import Post
from app.models.users import User
from app.routers.posts import router as posts_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router

# APP:
app = FastAPI()


# AutoCreation inexistrant tables:
Base.metadata.create_all(bind=engine)


#=========== ROUTERS ==========#
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)


# test endpoint root:
@app.get("/")
async def root():
    return {"message":"Hello World!"}