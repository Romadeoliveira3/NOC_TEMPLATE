from fastapi import APIRouter

from app.api.routes import pec_mock, utils

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(pec_mock.router)
