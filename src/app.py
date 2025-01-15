import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import router as api_router
from config import settings

logging.basicConfig(
    format=settings.logging.log_format,
)


origins = ["http://localhost:8000"]


app = FastAPI()
app.include_router(
    api_router,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )