from app.features.category.schema import CategoryCreate


class CategoryService:
    def __init__(self) -> None:
        pass

    def create(self, payload: CategoryCreate):
        print('validated')

    def get_all(self):
        return []
