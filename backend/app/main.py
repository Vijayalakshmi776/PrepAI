import logging

logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title='PrepAI', version='0.1.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):(5173|4173|8010|8000|3000)",
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(api_router, prefix=f'{settings.API_PREFIX}')


@app.get('/')
def root() -> dict:
    return {'message': 'PrepAI backend is online.'}


@app.get('/health')
def health() -> dict:
    return {'status': 'ok', 'message': 'PrepAI backend is online.'}
