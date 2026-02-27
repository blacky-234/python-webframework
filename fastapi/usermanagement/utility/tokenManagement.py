from datetime import datetime, timedelta,timezone
from jose import jwt,JWTError
from jose.exceptions import ExpiredSignatureError
"""
header.payload.signature

1. header:

{
  "alg": "HS256",
  "typ": "JWT"
}

2.payload :

{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}

3.
"""

class InvalidToken(Exception):
    pass

class Tokens:

    secret_key = "hello good body developments"
    algorithm = "HS256"
    
    @classmethod
    def create_access_token(cls,subject: dict, expires_delta: timedelta | None = None):
        """
        Access tokens expire after 15 minutes
        """
        to_encode = subject.copy()
        expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, cls.secret_key, algorithm=cls.algorithm)
        return encode_jwt
    
    @classmethod
    def create_refresh_token(cls,data:dict, expires_delta: timedelta | None = None):
        """
        Refresh tokens expire after 7 days
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(days=7))
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, cls.secret_key, algorithm=cls.algorithm)
        return encode_jwt
    
    
    @classmethod
    def verify_access_token(cls,token: str):
        try:
            payload = jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
            # token_data = auth_schema.TokenData(username=username)
            # return token_data
            return True
        except JWTError:
            return None
    
    @classmethod
    def token_payload(cls,token: str)->dict | None:
        try:
            payload = jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])
            return payload
        except ExpiredSignatureError:
            raise ExpiredSignatureError
        except JWTError:
            raise JWTError
        
    