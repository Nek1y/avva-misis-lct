from contextlib import asynccontextmanager
# import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import aioschedule

from src.routers.user_router import user_router
from src.routers.auth_router import auth_router
from src.routers.general_router import general_router
from src.database.db import db_create


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_create()
    yield

app: FastAPI = FastAPI(lifespan=lifespan, root_path='/api')

origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:3000',
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(general_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
