"""
This module defines API routes for client-related operations such as creating,
updating, retrieving, and deleting client data. It also includes prediction
functionality.
"""

import uuid
from fastapi import APIRouter, HTTPException
from mysql.connector import Error
from app.database import get_db
from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput, ClientData


def generate_client_id():
    """
    Generate a unique client ID using UUID4.
    """
    return str(uuid.uuid4())

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/predictions")
async def predict(data: PredictionInput):
    """
    Perform predictions based on the provided input data.

    Args:
        data (PredictionInput): The input data for the prediction model.

    Returns:
        dict: The calculated prediction results.
    """
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())


@router.post("/", response_model=ClientData)
async def create_client(client_data: ClientData):
    """
    Create a new client record in the system.

    Args:
        client_data (ClientData): The data for the new client to be created.

    Returns:
        ClientData: The newly created client data.

    Raises:
        HTTPException: Returns a 400 error if the client creation fails.
    """
    created_client = create_client_data(client_data.dict())
    if created_client:
        return created_client
    raise HTTPException(status_code=400, detail="Unable to create client")


@router.get("/{client_id}", response_model=ClientData)
async def get_client(client_id: str):
    """
    Retrieve a single client's data by their unique ID.

    Args:
        client_id (str): The unique ID of the client.

    Returns:
        ClientData: The client data corresponding to the specified ID.
    """
    client = get_client_data(client_id)
    if client:
        return client
    raise HTTPException(status_code=404, detail="Client not found")


@router.put("/{client_id}", response_model=ClientData)
async def update_client(client_id: str, updates: dict):
    """
    Update an existing client's data.

    Args:
        client_id (str): The unique ID of the client.
        updates (dict): A dictionary of fields to update.

    Returns:
        ClientData: The updated client data.
    """
    updated_client = update_client_data(client_id, updates)
    if updated_client:
        return updated_client
    raise HTTPException(status_code=404, detail="Unable to update client")


@router.delete("/{client_id}", response_model=dict)
async def delete_client(client_id: str):
    """
    Delete a client's data from the system.

    Args:
        client_id (str): The unique ID of the client.

    Returns:
        dict: A message indicating successful deletion.
    """
    if delete_client_data(client_id):
        return {"message": "Client deleted successfully"}
    raise HTTPException(status_code=404, detail="Client not found")


def create_client_data(client_data: dict):
    """
    Insert a new client record into the database with a unique ID.

    Args:
        client_data (dict): A dictionary containing the client data to be inserted.

    Returns:
        dict: The inserted client data with the generated client ID.
    """
    db_connection = next(get_db())
    cursor = db_connection.cursor()

    # Generate a unique client ID
    client_data["id"] = generate_client_id()

    # Define the SQL INSERT statement
    query = """
    INSERT INTO clients (id, name, email, age, gender)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        client_data["id"], client_data["name"], client_data["email"],
        client_data["age"], client_data["gender"]
    )

    try:
        cursor.execute(query, values)
        db_connection.commit()
        return client_data
    except Error as e:
        print(f"Database error: {e}")
        db_connection.rollback()
    finally:
        cursor.close()
    return None


def get_client_data(client_id: str):
    """
    Retrieve client data using the unique client ID.

    Args:
        client_id (str): The unique ID of the client.

    Returns:
        dict: The client data if found, or None otherwise.
    """
    db_connection = next(get_db())
    cursor = db_connection.cursor()
    query = "SELECT * FROM clients WHERE id = %s"
    cursor.execute(query, (client_id,))
    result = cursor.fetchone()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    if result:
        return dict(zip(column_names, result))
    return None


def update_client_data(client_id: str, updates: dict):
    """
    Update client data for the given client ID.

    Args:
        client_id (str): The unique client ID.
        updates (dict): The fields to update and their new values.

    Returns:
        dict: The updated client data if successful, or None if an error occurred.
    """
    db_connection = next(get_db())
    cursor = db_connection.cursor()

    update_fields = ", ".join([f"{key} = %s" for key in updates.keys()])
    query = f"UPDATE clients SET {update_fields} WHERE id = %s"
    values = tuple(updates.values()) + (client_id,)

    try:
        cursor.execute(query, values)
        db_connection.commit()
        return get_client_data(client_id)
    except Error as e:
        print(f"Database error: {e}")
        db_connection.rollback()
    finally:
        cursor.close()
    return None


def delete_client_data(client_id: str):
    """
    Delete client data for the given client ID.

    Args:
        client_id (str): The unique client ID.

    Returns:
        bool: True if the record was deleted, False otherwise.
    """
    db_connection = next(get_db())
    cursor = db_connection.cursor()
    query = "DELETE FROM clients WHERE id = %s"
    cursor.execute(query, (client_id,))
    db_connection.commit()
    success = cursor.rowcount > 0
    cursor.close()
    return success
