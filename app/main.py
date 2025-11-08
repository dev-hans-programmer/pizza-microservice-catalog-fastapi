from fastapi import FastAPI
from app.api.v1.routes import api_v1_router

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Hello server'}


app.include_router(router=api_v1_router, prefix='/api')
