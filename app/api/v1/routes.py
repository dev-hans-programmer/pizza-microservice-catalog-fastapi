from fastapi import APIRouter
from app.features.category.routes import category_router

api_v1_router = APIRouter(prefix='/v1')

api_v1_router.include_router(router=category_router)
