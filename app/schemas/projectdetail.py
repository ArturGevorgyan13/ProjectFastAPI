from pydantic import BaseModel, Field

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS IS THE BASE CLASS FOR PROJECT DETAIL
class ProjectDetailBase(BaseModel):
    status: str
    owner_company: str
    country: str

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS CLASS IS USED WHEN WE WANT TO EDIT PROJECT DETAIL
class ProjectDetailEdit(ProjectDetailBase):
    pass

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS CLASS IS USED WHEN WE WANT TO ADD PROJECT DETAIL
class ProjectDetailCreate(ProjectDetailBase):
    project_id: str

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS IS CURRENT WORKING CLASS FOR PROJECT DETAIL
class ProjectDetail(ProjectDetailBase):
    id: str = Field(..., alias="_id")
    project_id: str