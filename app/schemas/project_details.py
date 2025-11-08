from pydantic import BaseModel, Field
from datetime import datetime

class ProjectDetails(BaseModel):
    id: str = Field(..., alias="_id")
    owner_company: str
    country: str
    created_at: datetime