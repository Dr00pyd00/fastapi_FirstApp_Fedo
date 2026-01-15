from fastapi import FastAPI

# APP:
app = FastAPI()










# test endpoint root:
@app.get("/")
async def root():
    return {"message":"Hello World!"}