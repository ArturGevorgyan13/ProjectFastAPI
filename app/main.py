from fastapi import FastAPI
from app.routes import project

app = FastAPI()

app.include_router(project.router)