from app.database import projects_collection, projects_details
from app.schemas.project import ProjectSchema, ProjectCreate
from fastapi import APIRouter, HTTPException, Path, Response
from fastapi.responses import RedirectResponse
from datetime import datetime
from bson import ObjectId
import httpx

router = APIRouter()

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION GIVES ALL PROJECT DETAILS IN DATABASE
@router.get("/projects/details")
async def get_projects_details():
    docs = projects_details.find()

    details = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        details.append(doc)

    return details

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION FINDS ALL DETAILS OF PROVIDED ID PROJECT
@router.get("/projects/{id}/details")
async def get_project_details(id: str):

    print(f"This id is passed from user: {id}")

    try: 
        obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="invalid id format")

    doc = projects_details.find_one({"_id": obj_id})

    if not doc:
        raise HTTPException(status_code=404, detail="id is not found")
    
    doc["_id"] = str(doc["_id"])  

    return doc

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION ADDS ADDITIONAL DETAILS ABOUT PROJECT PROVIDED BY ID
@router.post("/projects/{id}/details")
async def add_project_details(id: str, owner_company: str = None, country: str = None):
    try:
        obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="invalid id format")
    
    doc = projects_details.find_one({"_id": obj_id})

    if not doc:
        raise HTTPException(status_code=404, detail="id is not found")
    
    new_details = {}

    if owner_company:
        new_details["owner_company"] = owner_company
    
    if country:
        new_details["country"] = country

    if not new_details:
        raise HTTPException(status_code=400, detail="no fields are mantioned")

    projects_details.update_one(

        {"_id": obj_id},
        {"$set": new_details}

    )

    return {"message": "Project details are updated"}

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION POSTS PROJECT TO DATABASE AND AUTOMATICALLY POSTS PROJECT'S DETAILS TO APPROPRIATE DATABASE
@router.post("/projects", response_model=ProjectSchema)
async def add_project(project: ProjectCreate):
    doc = project.model_dump()

    result = projects_collection.insert_one(doc)

    doc["_id"] = str(result.inserted_id)

    doc_details = dict()

    doc_details["_id"] = result.inserted_id
    doc_details["status"] = "active"
    doc_details["created_at"] = datetime.now()

    projects_details.insert_one(doc_details)

    return ProjectSchema.model_validate(doc)

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION GIVES ALL PROJECTS IN DATABASE
@router.get("/projects")
async def get_projects():
    projects = []

    for doc in projects_collection.find():
        doc["_id"] = str(doc["_id"])
        projects.append(ProjectSchema.model_validate(doc))

    return projects

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION FINDS PROJECT BY IT'S ID
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

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION GIVES THE INFORMATION FROM EXTRENAL URL
@router.get("/projects/news/{external_url:path}")
async def get_project_by_external_url(external_url: str = Path(..., description="external URL")):
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

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION EDITS THE PROJECT BY IT'S ID
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

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION DELETES PROJECT FROM DATABASE BY IT'S ID AND DELETES AUTOMATICALLY FROM THE DATABASE CONTAINING IT'S DETAILS
@router.delete("/projects/{id}")
async def delete_project(id: str):
        try:
            obj_id = ObjectId(id)
        except:
            raise HTTPException(status_code=400, detail="id is invalid")
        
        doc = projects_collection.delete_one({"_id": obj_id})

        if doc.deleted_count == 0:
            raise HTTPException(status_code=404, detail="id is not found")
        
        projects_details.delete_one({"_id": obj_id})

        return {"message": f"project with id {id} has been deleted"}