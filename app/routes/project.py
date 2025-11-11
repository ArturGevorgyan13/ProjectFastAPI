from app.database import projects_collection, projects_details
from app.schemas.project import Project, ProjectEdit, ProjectCreate
from fastapi import APIRouter, HTTPException, Path, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from datetime import datetime
from bson import ObjectId
import httpx
from typing import List

project_router = APIRouter()

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION POSTS PROJECT TO DATABASE
@project_router.post("/projects", response_model=Project)
async def add_project(project: ProjectCreate) -> Project:
    doc = project.model_dump()
    doc["created_at"] = datetime.now()

    result = projects_collection.insert_one(doc)

    doc["_id"] = str(result.inserted_id)

    return Project.model_validate(doc)

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION GIVES ALL PROJECTS IN DATABASE
@project_router.get("/projects", response_model=List[Project])
async def get_projects() -> List[Project]:
    projects = []

    for doc in projects_collection.find():
        doc["_id"] = str(doc["_id"])
        projects.append(Project.model_validate(doc))

    return projects

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION EDITS THE PROJECT BY IT'S ID
@project_router.put("/projects/{id}", response_model=Project)
async def edit_project(id: str, project: ProjectEdit) -> Project:
    try:
        obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="id is invalid")
    
    doc = projects_collection.find_one({"_id": obj_id})

    if not doc:
        raise HTTPException(status_code=404, detail="id is not found")
    
    projects_collection.update_one(

        {"_id": obj_id},
        {"$set": {"name": project.name, "description": project.description}}

    )

    updated_doc = projects_collection.find_one({"_id": obj_id})
    updated_doc["_id"] = str(updated_doc["_id"])

    return Project.model_validate(updated_doc)

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION FINDS PROJECT BY IT'S ID
@project_router.get("/projects/{id}", response_model=Project)
async def get_project(id: str) -> Project:
    try:
        obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="invalid id format")
    
    doc = projects_collection.find_one({"_id": obj_id})

    if not doc:
        raise HTTPException(status_code=404, detail="id is not found")
    
    doc["_id"] = str(doc["_id"])

    return Project.model_validate(doc)

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION DELETES PROJECT FROM DATABASE BY IT'S ID
@project_router.delete("/projects/{id}", response_model=dict)
async def delete_project(id: str) -> dict:
        try:
            obj_id = ObjectId(id)
        except:
            raise HTTPException(status_code=400, detail="id is invalid")
        
        doc = projects_collection.delete_one({"_id": obj_id})

        if doc.deleted_count == 0:
            raise HTTPException(status_code=404, detail="id is not found")

        return {"message": f"project with id {id} has been deleted"}

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION GIVES THE INFORMATION FROM EXTRENAL URL
@project_router.get("/projects/news/{external_url:path}", response_class=HTMLResponse)
async def get_project_by_external_url(external_url: str = Path(..., description="external URL")) -> HTMLResponse:
    from urllib.parse import unquote

    print(f"This is quoted url: {external_url}")

    u = unquote(external_url)

    print(f"This is unquoted url: {u}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(u)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"cannot reach external URL: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"error from external service: {e}")
    
    return Response(content=response.text, media_type="text/html")