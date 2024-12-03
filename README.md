This will contain the model used for the project that based on the input information will give the social workers the clients baseline level of success and what their success will be after certain interventions.

The model works off of dummy data of several combinations of clients alongside the interventions chosen for them as well as their success rate at finding a job afterward. The model will be updated by the case workers by inputing new data for clients with their updated outcome information, and it can be updated on a daily, weekly, or monthly basis.

This also has an API file to interact with the front end, and logic in order to process the interventions coming from the front end. This includes functions to clean data, create a matrix of all possible combinations in order to get the ones with the highest increase of success, and output the results in a way the front end can interact with.


Endpoints
1. Create a New Client
URL: /clients/
Method: POST
Description: Creates a new client record. A unique id for each client will be auto-generated and can be future used when getting, updating and deleting a client record.
Request Body:
{ "id": "",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "gender": "male"
}
Response:
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "gender": "male"
}
Error Response:
400: Unable to create client.


2. Retrieve Client Data
URL: /clients/{client_id}
Method: GET
Description: Retrieves data for a specific client by their unique ID.
Path Parameter:
client_id: The unique ID of the client.
Response:
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "gender": "male"
}
Error Response:
404: Client not found.

3. Update Client Data
URL: /clients/{client_id}
Method: PUT
Description: Updates a client's information.
Path Parameter:
client_id: The unique ID of the client.
Request Body:
{
  "email": "new.email@example.com",
  "age": 35
}
Response:
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "new.email@example.com",
  "age": 35,
  "gender": "male"
}
Error Response:
404: Unable to update client.

4. Delete Client
URL: /clients/{client_id}
Method: DELETE
Description: Deletes a client's data by their unique ID.
Path Parameter:
client_id: The unique ID of the client.
Response:
{
  "message": "Client deleted successfully"
}
Error Response:
404: Client not found.
