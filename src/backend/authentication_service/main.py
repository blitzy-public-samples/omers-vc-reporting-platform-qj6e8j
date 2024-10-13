"""
Main entry point for the authentication service, responsible for initializing the FastAPI application,
setting up routes, and configuring middleware for handling authentication requests.

This module addresses the following requirement:
- Authentication and Authorization Implementation (Technical Requirements/Feature 4)
"""

# Import FastAPI and necessary modules
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import internal dependencies
from src.backend.authentication_service.config import load_config
from src.backend.authentication_service.app.security import generate_token, validate_token

# FastAPI version: 0.68.1
# Uvicorn version: 0.15.0

def create_app() -> FastAPI:
    """
    Initializes the FastAPI application, sets up routes, and configures middleware.

    Returns:
        FastAPI: The initialized FastAPI application instance.
    """
    # Load configuration settings
    config = load_config()

    # Initialize the FastAPI application
    app = FastAPI(
        title="Authentication Service",
        description="API for handling authentication and token generation",
        version="1.0.0",
        debug=config['DEBUG']
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this in production to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize OAuth2 password bearer for token authentication
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @app.post("/token")
    async def login_for_access_token(username: str, password: str):
        """
        Endpoint for user authentication and token generation.

        Args:
            username (str): The user's username.
            password (str): The user's password.

        Returns:
            dict: A dictionary containing the access token and token type.

        Raises:
            HTTPException: If authentication fails.
        """
        # TODO: Implement actual user authentication logic here
        # For demonstration purposes, we'll use a dummy check
        if username == "testuser" and password == "testpassword":
            token = generate_token(username)
            return {"access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @app.get("/protected")
    async def protected_route(token: str = Depends(oauth2_scheme)):
        """
        A protected route that requires a valid token for access.

        Args:
            token (str): The JWT token provided in the request header.

        Returns:
            dict: A message indicating successful authentication.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        try:
            user_id = validate_token(token)
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return {"message": f"Hello, {user_id}! This is a protected route."}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return app

# Entry point
if __name__ == "__main__":
    app = create_app()
    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)