import pytest
import jwt
from datetime import datetime, timedelta
from src.backend.authentication_service.app.security import generate_token, validate_token
from src.backend.authentication_service.config import load_config

# Retrieve the configuration settings
config = load_config()

@pytest.mark.parametrize("user_id", ["user123", "admin456", "test789"])
def test_generate_token(user_id):
    """
    Test the generate_token function to ensure it creates a valid JWT token.
    
    This test addresses the requirement:
    'Authentication and Authorization Implementation' located in
    'Technical Requirements/Feature 4: Authentication and Authorization Implementation'
    
    Args:
        user_id (str): Sample user ID to generate token for.
    
    Returns:
        bool: True if the token is generated correctly, False otherwise.
    """
    # Generate token
    token = generate_token(user_id)
    
    # Verify that the token is a non-empty string
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode the token and verify its contents
    try:
        decoded_token = jwt.decode(token, config['SECRET_KEY'], algorithms=["HS256"])
        assert decoded_token["sub"] == user_id
        assert "exp" in decoded_token
        
        # Check if the expiration time is set correctly
        exp_time = datetime.fromtimestamp(decoded_token["exp"])
        expected_exp_time = datetime.utcnow() + timedelta(minutes=config['TOKEN_EXPIRATION'])
        assert abs((exp_time - expected_exp_time).total_seconds()) < 1  # Allow 1 second difference
        
        return True
    except jwt.PyJWTError:
        pytest.fail("Failed to decode the generated token")
        return False

@pytest.mark.parametrize("user_id", ["user123", "admin456", "test789"])
def test_validate_token(user_id):
    """
    Test the validate_token function to ensure it correctly validates a JWT token and extracts the user ID.
    
    This test addresses the requirement:
    'Authentication and Authorization Implementation' located in
    'Technical Requirements/Feature 4: Authentication and Authorization Implementation'
    
    Args:
        user_id (str): Sample user ID to generate and validate token for.
    
    Returns:
        bool: True if the token is validated correctly and the user ID is extracted, False otherwise.
    """
    # Generate a valid token
    valid_token = generate_token(user_id)
    
    # Test with valid token
    try:
        extracted_user_id = validate_token(valid_token)
        assert extracted_user_id == user_id
    except Exception as e:
        pytest.fail(f"Failed to validate a valid token: {str(e)}")
        return False
    
    # Test with invalid token
    invalid_token = "invalid.token.string"
    with pytest.raises(jwt.PyJWTError):
        validate_token(invalid_token)
    
    # Test with expired token
    config['TOKEN_EXPIRATION'] = -1  # Set expiration to negative value to create an expired token
    expired_token = generate_token(user_id)
    with pytest.raises(jwt.ExpiredSignatureError):
        validate_token(expired_token)
    
    return True

# Additional tests can be added here to cover more scenarios and edge cases