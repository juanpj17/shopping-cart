from fastapi import HTTPException, Depends, status
from ..providers.jwt_services import JwtService
from ..providers.oauth2_services import oauth2_scheme
from ...application.exceptions.token_is_empty import EmptyTokenError
from typing import Annotated

def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if token is None:
        raise EmptyTokenError()
    try:
        decoded_token = JwtService.validate_token(token, True)
        return {"id": decoded_token.get("id"), "role": decoded_token.get("role")}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al procesar el token",
        )
        