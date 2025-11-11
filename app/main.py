from fastapi import FastAPI
from app.routes import project, projectdetail

app = FastAPI()

app.include_router(project.project_router)
app.include_router(projectdetail.project_detail_router)