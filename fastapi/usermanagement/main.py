from fastapi import FastAPI
from src.userapp.urls import user
from utility.middleware import jwt_decode_middleware

app = FastAPI()
app.middleware("http")(jwt_decode_middleware)
app.include_router(user)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}