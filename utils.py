import jwt
from config import ApplicationConfig


def jwt_decode(token):
    try:
        decoded = jwt.decode(token, ApplicationConfig.SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"error": "Token inválido"}