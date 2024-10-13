# src/backend/authentication_service/app/security.py

import jwt
from datetime import datetime, timedelta
from typing import Optional

# PyJWT version 2.3.0
from jwt import PyJWTError

from src.backend.authentication_service.config import load_config

# Load configuration settings
config = load_config()

def generate_token(user_id: str) -> str:
    """
    Generates a JWT token for a given user ID, encoding it with a secret key and setting an expiration time.

    This function addresses the requirement:
    'Authentication and Authorization Implementation' located in 'Technical Requirements/Feature 4: Authentication and Authorization Implementation'
    which states: 'Implement secure authentication and authorization mechanisms to control access to the backend platform and its resources.'

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        str: A JWT token encoded with the user ID and expiration time.
    """
    # Load configuration settings
    secret_key = config['SECRET_KEY']
    token_expiration = config['TOKEN_EXPIRATION']

    # Create a payload containing the user_id and expiration time
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=token_expiration)
    }

    # Encode the payload using PyJWT with the SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token

def validate_token(token: str) -> Optional[str]:
    """
    Validates a given JWT token, ensuring it is correctly signed and not expired, and extracts the user ID.

    This function addresses the requirement:
    'Authentication and Authorization Implementation' located in 'Technical Requirements/Feature 4: Authentication and Authorization Implementation'
    which states: 'Implement secure authentication and authorization mechanisms to control access to the backend platform and its resources.'

    Args:
        token (str): The JWT token to validate.

    Returns:
        Optional[str]: The user ID extracted from the token if valid, None otherwise.
    """
    # Load configuration settings
    secret_key = config['SECRET_KEY']

    try:
        # Decode the token using PyJWT with the SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        # Extract and return the user ID from the token payload
        return payload.get("sub")
    except PyJWTError:
        # If the token is invalid or expired, return None
        return None

# Additional helper functions can be added here as needed for enhanced security features