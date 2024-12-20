from fastapi.responses import JSONResponse
import jwt 
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.env.template')
load_dotenv(dotenv_path=env_path)


class JwtService():
    
    def generateToken(id: str, role: str) -> str:
        date = datetime.now()
        expires = date + timedelta(minutes=40)
        token =  jwt.encode(payload = {"id": id, "role": role, "exp": expires.timestamp()}, key=getenv("SECRET_KEY"), algorithm="HS256")
        return token
    
    def validate_token(token: str, output: False):
        try:
            if output:
                return jwt.decode(token, key=getenv("SECRET_KEY"), algorithms=["HS256"])
            jwt.decode(token, key=getenv("SECRET_KEY"), algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})
        except jwt.exceptions.ExpiredSignatureError:
            return JSONResponse(status_code=400, content={"error": "Token expired"})
