from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/api/ping", response_class=PlainTextResponse)
def ping_handler():
    return Response(content="ok", status_code=200)
