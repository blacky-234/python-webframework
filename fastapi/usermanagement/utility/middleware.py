from fastapi import Request
from .tokenManagement import Tokens



async def jwt_decode_middleware(request:Request,call_next):
    request.state.user = None


    auth_header = request.headers.get("Authorizations")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = Tokens.token_payload(token)
            request.state.user = payload
        except:
            pass
    return await call_next(request)