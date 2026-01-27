from typing import Union

from fastapi import FastAPI
from src.users import user_routes
from src.users import user_models
import database
from src.auth import auth_routes

# Create database tables - usually at app startup (better to use migrations!)
# user_models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(debug=True)

app.include_router(user_routes.user_router)
app.include_router(auth_routes.auth)




@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}