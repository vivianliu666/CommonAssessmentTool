"""
Main application module for the FastAPI application.

This module sets up the FastAPI app, includes the clients router for handling client-related
endpoints, and configures CORS middleware to allow cross-origin requests.

Modules and Features:
- FastAPI: Main application framework for building APIs.
- CORSMiddleware: Configured to allow requests from all origins, methods, and headers.
- Clients Router: Handles client-related operations, included via `app.clients.router`.

Usage:
Start the FastAPI application using a server like Uvicorn or Hypercorn.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.clients.router import router as clients_router

app = FastAPI()

# Set API endpoints on router
app.include_router(clients_router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)
