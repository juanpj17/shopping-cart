from fastapi import APIRouter, HTTPException, Depends

from apps.users.application.commands.update_user_command.update_manager import UpdateManagerService
from .Dtos import ManagerDto, ClientDto, SuperAdminDto, LoginDto
from .Dtos.get_user_by_id_dto import GetUserByIdDto
from ...application.commands.register_user_command.register_user import RegisterUserService
from ...application.queries.get_all_users_query.get_all_users import GetAllUsersService
from ...application.queries.get_user_by_id.get_user_by_id import GetUserByIdService
from apps.auth.application.commands.login_command.login_service import LoginService
from ..repositories.postgres_user_repository import PostgreUserRepository
from ..models.user_model import UserModel
from ....auth.infrastructure.middlewares.verify_user_role import get_user
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ...application.commands.update_user_command.update_user import UpdateUserService
from .Dtos.update_user_dto import UpdateUserDto

router = APIRouter(tags=['User'])
user_model = UserModel
repository = PostgreUserRepository(user_model)
endpoint_called = False

@router.post("/users/create_superadmin")
def register_superadmin(registerDto: SuperAdminDto):
    global endpoint_called
    if endpoint_called:
        raise HTTPException(status_code=400, detail="This endpoint can only be executed once.")
    endpoint_called = True
    service = RegisterUserService(repository)
    response = service.execute(registerDto)
    return response.unwrap()

@router.post('/users/register')
def register_client(registerDto: ClientDto):
    service = RegisterUserService(repository)
    response = service.execute(registerDto)
    return response.unwrap()

@router.put('/users/{user_id}')
def update_client(id:str, data: UpdateUserDto):
    service = UpdateUserService(repository)
    response = service.execute(data)
    return response.unwrap()

@router.put('/users/managers/{manager_id}')
def update_client(id:str, data: ManagerDto, user: dict = Depends(get_user)):
    if user.get("role") != "Superadmin":
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = UpdateManagerService(repository)
    response = service.execute(id, data)
    return response.unwrap()

@router.post('/users/managers')
def register_manager(
    registerDto: ManagerDto,
    user: dict = Depends(get_user)
    ):
    if user.get("role") != "Superadmin":
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = RegisterUserService(repository)
    response = service.execute(registerDto)
    return response.unwrap()

@router.get('/users/managers')
def get_all_users(user: dict = Depends(get_user)):
    if user.get("role") != "Superadmin":
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = GetAllUsersService(repository)
    response = service.execute()
    return response.unwrap()

@router.post('/token', include_in_schema = False)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    service = LoginService(repository)
    loginDto = LoginDto(username = form_data.username, password = form_data.password)
    response = service.execute(loginDto)
    return response.unwrap()

@router.get("/users/me")
def get_current_user(user: dict = Depends(get_user)):
    if user is None: 
        raise HTTPException(status_code=404, detail="You are not logged")
    service = GetUserByIdService(repository)
    data = GetUserByIdDto( id = user.get("id"))
    response = service.execute(data) 
    return response.unwrap()