from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS IS MY BASE PROJECT CLASS, EVERY PROJECT MUST CONTAIN THIS AS MINIMAL
class ProjectBase(BaseModel):
    name: str
    description: str

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS IS MY CLASS THAT IS USED TO CREATE PROJECT
class ProjectCreate(ProjectBase):
    pass

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS CLASS IS MY WORKING PROJECT'S CLASS, IT IS USED TO BE ADDED INTO MY DATABASE
class ProjectSchema(ProjectBase):
    id: str = Field(..., alias="_id")

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS IS MY BASE CLASS ABOUT PROJECT DETAILS, EVERY PROJECT DETAIL MUST HAVE THESE FIELDS
class ProjectDetailBase(BaseModel):
    status: str
    created_at: datetime

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS IS MY WORKING PROJECT DETAILS CLASS
class ProjectDetail(ProjectDetailBase):
    id: str = Field(..., alias="_id")
    project_id: str
    owner_company: Optional[str] = None
    country: Optional[str] = None

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS IS USED FOR CREATING(POST) NEW DETAILS ABOUT PROJECT
class ProjectDetailCreate(BaseModel):
    owner_company: Optional[str] = None
    country: Optional[str] = None