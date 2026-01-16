from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.posts import Post
from app.routers.posts import router as posts_router

# APP:
app = FastAPI()


# AutoCreation inexistrant tables:
Base.metadata.create_all(bind=engine)


#=========== ROUTERS ==========#
app.include_router(posts_router)


# test endpoint root:
@app.get("/")
async def root():
    return {"message":"Hello World!"}