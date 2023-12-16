from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import api

# Initializing
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
    allow_credentials=True,
    allow_methods={"OPTIONS", "GET", "POST", "DELETE", "PUT"},
    allow_headers={"*"},
)


@app.on_event("startup")
def on_startup():
    from app import models
    from app.database import engine

    models.Base.metadata.create_all(bind=engine)


app.include_router(api.router)
