from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title='PrepAI', version='0.1.0')
app.include_router(api_router, prefix=f'{settings.API_PREFIX}')

@app.get('/')
def root() -> dict:
    return {'message': 'PrepAI backend is online.'}
