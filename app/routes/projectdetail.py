from app.database import projects_details, projects_collection
from app.schemas.projectdetail import ProjectDetail, ProjectDetailEdit, ProjectDetailCreate
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List

project_detail_router = APIRouter()

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION CREATES PROJECT DETAIL IN APPROPRIATE COLLECTION
@project_detail_router.post("/projects/details", response_model=ProjectDetail)
async def add_project_details(projectdetail: ProjectDetailCreate) -> ProjectDetail:
    try:
        project_obj_id = ObjectId(projectdetail.project_id)
    except:
        raise HTTPException(status_code=400, detail="id is invalid")
    
    project = projects_collection.find_one({"_id": project_obj_id})

    if not project:
        raise HTTPException(status_code=404, detail="id is not found")

    doc = projectdetail.model_dump()
    doc["project_id"] = project_obj_id

    result = projects_details.insert_one(doc)

    doc["_id"] = str(result.inserted_id)
    doc["project_id"] = str(doc["project_id"])

    return ProjectDetail.model_validate(doc)

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION GIVES ALL PROJECT DETAILS IN DATABASE
@project_detail_router.get("/projects/all/details", response_model=List[ProjectDetail])
async def get_projects_details() -> List[ProjectDetail]:
    docs = projects_details.find()

    details = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        doc["project_id"] = str(doc["project_id"])
        details.append(doc)

    return details

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION EDITS THE DETAILS OF PROJECT OF PROVIDED ID
@project_detail_router.put("/projects/{id}/details", response_model=ProjectDetail)
async def edit_project_details(id: str, projectdetail: ProjectDetailEdit) -> ProjectDetail:
    try:
        project_obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="id is invalid")

    doc = projects_details.find_one({"project_id": project_obj_id})

    if not doc:
        raise HTTPException(status_code=404, detail="id is not found")

    projects_details.update_one(
        {"project_id": project_obj_id},
        {"$set": projectdetail.model_dump()}
    )

    updated = projects_details.find_one({"project_id": project_obj_id})
    updated["_id"] = str(updated["_id"])
    updated["project_id"] = str(updated["project_id"])

    return ProjectDetail.model_validate(updated)

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION FINDS ALL DETAILS OF PROVIDED ID PROJECT
@project_detail_router.get("/projects/{id}/details", response_model=ProjectDetail)
async def get_project_details(id: str) -> ProjectDetail:

    print(f"This id is passed from user: {id}")

    try: 
        obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="invalid id format")

    doc = projects_details.find_one({"project_id": obj_id})

    if not doc:
        raise HTTPException(status_code=404, detail="id is not found")
    
    doc["_id"] = str(doc["_id"])  
    doc["project_id"] = str(doc["project_id"])

    return ProjectDetail.model_validate(doc)

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS FUNCTION DELETE PROJECT DETAIL FROM APPROPRIATE COLLECTION IN DATABASE
@project_detail_router.delete("/projects/{id}/details", response_model=dict)
async def delete_project_details(id: str) -> dict:
    try:
        project_obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="id is invalid")
    
    doc = projects_details.delete_one({"project_id": project_obj_id})

    if doc.deleted_count == 0:
        raise HTTPException(status_code=404, detail="id is not found")
    
    return {"message": f"details of {id} project has been deleted"}