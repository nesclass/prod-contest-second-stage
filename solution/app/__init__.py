from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.exceptions import APIError
from app.database import init_database

from app.routes.ping import router as ping_router
from app.routes.country import router as country_router
from app.routes.auth import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.friend import router as friend_router
from app.routes.post import router as post_router

app = FastAPI()

app.include_router(ping_router)
app.include_router(country_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(friend_router)
app.include_router(post_router)


@app.on_event("startup")
def on_startup():
    init_database()


@app.exception_handler(APIError)
def api_error_handler(request: Request, error: APIError):
    return JSONResponse(
        content={"reason": error.reason},
        status_code=error.status_code
    )


@app.exception_handler(RequestValidationError)
def request_validation_error_handler(request: Request, error: RequestValidationError):
    return JSONResponse(
        content={"reason": str(error)},
        status_code=400
    )
