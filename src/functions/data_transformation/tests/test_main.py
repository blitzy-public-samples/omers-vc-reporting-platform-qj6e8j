import pytest
import json
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from src.functions.data_transformation.main import transform_data

# Importing the function to be tested
# Note: Assuming the function is in the main.py file in the same directory

@pytest.fixture
def mock_input_data():
    return {
        "company_id": "reciLI8sBuJE9vEAv",
        "reporting_year": 2022,
        "reporting_quarter": 4,
        "currency": "USD",
        "total_revenue": 4194199.0,
        "recurring_revenue": 3912138.0,
        "gross_profit": 2730244.0,
        "sales_marketing_expense": 1470828.0,
        "total_operating_expense": 7195136.0,
        "ebitda": -4464892.0,
        "net_income": -4339102.0,
        "cash_burn": -4464892.0,
        "cash_balance": 32407138.0,
        "debt_outstanding": None,
        "employees": 1,
        "customers": None
    }

@pytest.fixture
def mock_fx_rates():
    return {
        "USD": 1.0,
        "CAD": 1.25,
        "EUR": 0.85
    }

@patch('requests.get')
def test_transform_data(mock_get, mock_input_data, mock_fx_rates):
    """
    Tests the transform_data function to ensure it correctly performs data transformation tasks.
    
    This test verifies that:
    1. The function correctly retrieves FX rates
    2. Currency conversion is performed accurately
    3. Derivative metrics are calculated correctly
    
    Requirements addressed:
    - Data Transformation Processes (Technical Requirements/Feature 3: Data Transformation Processes)
    """
    # Mock the FX rates API response
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": mock_fx_rates}
    mock_get.return_value = mock_response

    # Call the transform_data function
    result = transform_data(mock_input_data)

    # Assert that the function returns a dictionary
    assert isinstance(result, dict)

    # Verify currency conversion
    assert 'total_revenue_CAD' in result
    assert 'total_revenue_EUR' in result

    # Check USD values (should be unchanged)
    assert result['total_revenue'] == mock_input_data['total_revenue']

    # Check CAD conversion
    assert result['total_revenue_CAD'] == pytest.approx(mock_input_data['total_revenue'] * mock_fx_rates['CAD'])

    # Check EUR conversion
    assert result['total_revenue_EUR'] == pytest.approx(mock_input_data['total_revenue'] * mock_fx_rates['EUR'])

    # Verify derivative calculations (example with ARR)
    expected_arr = mock_input_data['recurring_revenue'] * 4  # Assuming ARR is calculated as 4 * quarterly recurring revenue
    assert result['arr'] == pytest.approx(expected_arr)

    # Verify other derivative metrics are present
    derivative_metrics = [
        'arr', 'recurring_percentage_revenue', 'revenue_per_fte', 'gross_profit_per_fte',
        'sales_marketing_percentage_revenue', 'total_operating_percentage_revenue',
        'gross_profit_margin', 'runway_months'
    ]
    for metric in derivative_metrics:
        assert metric in result

@pytest.mark.parametrize("currency", ["USD", "CAD", "EUR"])
def test_currency_conversion(mock_input_data, mock_fx_rates, currency):
    """
    Verifies that the currency conversion logic in transform_data is accurate.
    
    Requirements addressed:
    - Data Transformation Processes (Technical Requirements/Feature 3: Data Transformation Processes)
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": mock_fx_rates}
        mock_get.return_value = mock_response

        result = transform_data(mock_input_data)

        assert f'total_revenue_{currency}' in result
        for key, value in mock_input_data.items():
            if isinstance(value, (int, float)):
                assert result[f'{key}_{currency}'] == pytest.approx(value * mock_fx_rates[currency])

def test_derivative_calculations(mock_input_data):
    """
    Ensures that derivative financial metrics are calculated correctly.
    
    Requirements addressed:
    - Data Transformation Processes (Technical Requirements/Feature 3: Data Transformation Processes)
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"USD": 1.0, "CAD": 1.0, "EUR": 1.0}}
        mock_get.return_value = mock_response

        result = transform_data(mock_input_data)

        # Test ARR calculation
        assert result['arr'] == pytest.approx(mock_input_data['recurring_revenue'] * 4)

        # Test recurring percentage revenue
        assert result['recurring_percentage_revenue'] == pytest.approx(
            (mock_input_data['recurring_revenue'] / mock_input_data['total_revenue']) * 100
        )

        # Test revenue per FTE
        assert result['revenue_per_fte'] == pytest.approx(
            mock_input_data['total_revenue'] / mock_input_data['employees']
        )

        # Test gross profit margin
        assert result['gross_profit_margin'] == pytest.approx(
            (mock_input_data['gross_profit'] / mock_input_data['total_revenue']) * 100
        )

        # Add more assertions for other derivative metrics as needed

def test_error_handling():
    """
    Tests error handling in the transform_data function.
    
    Requirements addressed:
    - Data Transformation Processes (Technical Requirements/Feature 3: Data Transformation Processes)
    """
    with patch('requests.get') as mock_get:
        # Simulate a failed API request
        mock_get.side_effect = Exception("API request failed")

        with pytest.raises(Exception):
            transform_data({})

def test_input_validation():
    """
    Tests input validation in the transform_data function.
    
    Requirements addressed:
    - Data Transformation Processes (Technical Requirements/Feature 3: Data Transformation Processes)
    """
    invalid_input = {
        "company_id": "reciLI8sBuJE9vEAv",
        "reporting_year": "invalid",  # Should be an integer
        "currency": "INVALID_CURRENCY"
    }

    with pytest.raises(ValueError):
        transform_data(invalid_input)

# Add more test cases as needed to cover edge cases and additional scenarios