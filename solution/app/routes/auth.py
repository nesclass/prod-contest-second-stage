from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.exceptions import APIError
from app.utils import generate_token
from app.repositories.user import UserRepository, get_user_repository
from app.repositories.country import CountryRepository, get_country_repository
from app.schemas.user import UserSchema, RegisterForm, RegisterSchema, LoginForm, LoginSchema

router = APIRouter()


@router.post("/api/auth/register", status_code=201, response_model_exclude_none=True)
def register_handler(
    form: RegisterForm,
    user_repository: UserRepository = Depends(get_user_repository),
    country_repository: CountryRepository = Depends(get_country_repository)
) -> RegisterSchema:
    if not country_repository.find_country_by_alpha2(form.countryCode):
        raise APIError(status_code=400, reason="Страны с указанным кодом не существует")
    elif user_repository.find_by_credentials(login=form.login, email=form.email, phone=form.phone):
        raise APIError(status_code=409, reason="Пользователь с указанными регистрационными данными уже существует")
    
    user = user_repository.create(
        login=form.login,
        email=form.email,
        password=form.password,
        countryCode=form.countryCode,
        isPublic=form.isPublic,
        phone=form.phone,
        image=form.image    
    )
    
    return RegisterSchema(profile=UserSchema.model_validate(user))


@router.post("/api/auth/sign-in")
def sign_in_handler(
    form: LoginForm,
    user_repository: UserRepository = Depends(get_user_repository)
) -> LoginSchema:
    if not user_repository.find_by_password(login=form.login, password=form.password):
        raise APIError(status_code=401, reason="Неверный логин или пароль")
    
    token = generate_token(login=form.login, password=form.password)
    return LoginSchema(token=token)
