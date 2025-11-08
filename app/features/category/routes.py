from fastapi import APIRouter, Depends
from app.features.category.service import CategoryService
from app.features.category.schema import CategoryCreate, CategoryRead


category_router = APIRouter(prefix='/category')


def get_category_service():
    return CategoryService()


@category_router.get('/', response_model=list[CategoryRead])
def list_categories(service: CategoryService = Depends(get_category_service)):
    categories = service.get_all()
    return categories


@category_router.post('/', response_model=CategoryCreate)
def create_category(
    payload: CategoryCreate, service: CategoryService = Depends(get_category_service)
):
    service.create(payload)
    return payload
