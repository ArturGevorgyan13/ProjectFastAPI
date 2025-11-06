from pydantic import BaseModel, Field
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class ProjectSchema(ProjectBase):
    id: str = Field(..., alias="_id")
    status: str
    created_at: datetime