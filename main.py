from fastapi import FastAPI
from app.routes import cleaning

app = FastAPI()
app.include_router(cleaning.router)
