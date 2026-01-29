from fastapi import FastAPI
from src.userapp.urls import user

app = FastAPI()
app.include_router(user)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}