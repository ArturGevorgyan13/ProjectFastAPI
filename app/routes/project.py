from app.database import projects_collection
from app.schemas.project import ProjectSchema, ProjectCreate
from app.schemas.project_details import ProjectDetails
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from bson import ObjectId
import httpx

router = APIRouter()

# todo
@router.get("/projects/{project_id}/details")
async def get_project_details(
    project_id: str
):
    doc = projects_collection.find_one({"_id": ObjectId(project_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="id is not found")
    doc["_id"] = str(doc["_id"])
    return ProjectDetails.model_validate(doc)

# todo
# @router.post("/projects/{project_id}/details")

@router.post("/projects", response_model=ProjectSchema)
async def add_project(project: ProjectCreate):
    doc = project.model_dump()

    doc["status"] = "active"
    doc["created_at"] = datetime.now()

    result = projects_collection.insert_one(doc)

    doc["_id"] = str(result.inserted_id)

    return ProjectSchema.model_validate(doc)

@router.get("/projects")
async def get_projects():
    projects = []

    for doc in projects_collection.find():
        doc["_id"] = str(doc["_id"])
        projects.append(ProjectSchema.model_validate(doc))

    return projects

# todo @router.get("/projects/news/{external_url}")
@router.get("/projects/news")
async def get_project_by_external_url(
    external_url: str = Query() # queriic tanel path parameter
):
    from urllib.parse import unquote

    u = unquote(external_url) # berel normal tesqi ???

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(u)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"cannot reach external URL: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"error from external service: {e}")
        
    try:
        return response
    except ValueError:
        raise HTTPException(status_code=502, detail="external service returned invalid JSON")

    # return processed_data


@router.get("/projects/{id}")
async def get_project(id: str):
    try:
        obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="invalid id format")
    
    doc = projects_collection.find_one({"_id": obj_id})

    if not doc:
        raise HTTPException(status_code=404, detail="id is not found")
    
    doc["_id"] = str(doc["_id"])

    return ProjectSchema.model_validate(doc)

@router.put("/projects/{id}")
async def edit_project(id: str, project: ProjectCreate):
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

    return ProjectSchema.model_validate(updated_doc)

@router.delete("/projects/{id}")
async def delete_project(id: str):
        try:
            obj_id = ObjectId(id)
        except:
            raise HTTPException(status_code=400, detail="id is invalid")
        
        doc = projects_collection.delete_one({"_id": obj_id})

        if doc.deleted_count == 0:
            raise HTTPException(status_code=404, detail="id is not found")

        return {"message": f"project with id {id} has been deleted"}