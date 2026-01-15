from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.posts import Post

# APP:
app = FastAPI()


# AutoCreation inexistrant tables:
Base.metadata.create_all(bind=engine)



# test endpoint root:
@app.get("/")
async def root():
    return {"message":"Hello World!"}