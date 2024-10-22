from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.clients.service.logic import interpret_and_calculate, get_client_data, update_client_data, delete_client_data
from app.clients.schema import PredictionInput

# Define a Pydantic model for client data
class ClientData(BaseModel):
    age: int
    gender: int
    work_experience: int
    canada_workex: int
    dep_num: int
    canada_born: int
    citizen_status: int
    level_of_schooling: int
    fluent_english: int
    reading_english_scale: int
    speaking_english_scale: int
    writing_english_scale: int
    numeracy_scale: int
    computer_scale: int
    transportation_bool: int
    caregiver_bool: int
    housing: int
    income_source: int
    felony_bool: int
    attending_school: int
    currently_employed: int
    substance_use: int
    time_unemployed: int
    need_mental_health_support_bool: int
    employment_assistance: int
    life_stabilization: int
    retention_services: int
    specialized_services: int
    employment_related_financial_supports: int
    employer_financial_supports: int
    enhanced_referrals: int
    success_rate: int

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())

@router.get("/", response_model=ClientData)
async def get_client(age: int, gender: int, work_experience: int):
    """
    Retrieve a single client's data by their unique attributes.

    Args:
        age (int): The age of the client.
        gender (int): The gender of the client.
        work_experience (int): The work experience of the client.

    Returns:
        ClientData: The client data corresponding to the specified attributes.

    Raises:
        HTTPException: Returns a 404 error if no client is found with the provided attributes.
    """
    client = get_client_data(age, gender, work_experience)
    if client:
        return client
    else:
        raise HTTPException(status_code=404, detail="Client not found")

@router.put("/", response_model=ClientData)
async def update_client(client_update: ClientData):
    """
    Update an existing client's data.

    Args:
        client_update (ClientData): A model containing the client's updated data.

    Returns:
        ClientData: The updated client data.

    Raises:
        HTTPException: Returns a 404 error if no client is found with the provided attributes, or if the update fails.
    """
    updated_client = update_client_data(client_update.dict())
    if updated_client:
        return updated_client
    else:
        raise HTTPException(status_code=404, detail="Unable to update client")

@router.delete("/", response_model=dict)
async def delete_client(age: int, gender: int, work_experience: int):
    """
    Delete a client's data from the system.

    Args:
        age (int): The age of the client.
        gender (int): The gender of the client.
        work_experience (int): The work experience of the client.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: Returns a 404 error if no client is found with the provided attributes, or if the deletion fails.
    """
    if delete_client_data(age, gender, work_experience):
        return {"message": "Client deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Client not found")
