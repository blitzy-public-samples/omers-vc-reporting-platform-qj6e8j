import azure.functions as func
import requests
import pandas as pd
import numpy as np
import logging
from typing import Dict
import os

# External library versions (for reference)
# azure-functions==1.11.2
# requests==2.26.0
# pandas==1.3.5
# numpy==1.21.5

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global constants
FUNCTION_NAME = "data_transformation"
FX_RATES_API_URL = os.environ.get("FX_RATES_API_URL", "https://api.exchangerates.example.com/latest")
FX_RATES_API_KEY = os.environ.get("FX_RATES_API_KEY")

def get_fx_rates() -> Dict[str, float]:
    """
    Retrieve the latest foreign exchange rates using the requests library.
    
    Returns:
        Dict[str, float]: A dictionary of currency codes and their exchange rates.
    
    Raises:
        requests.RequestException: If there's an error fetching the FX rates.
    """
    try:
        response = requests.get(FX_RATES_API_URL, headers={"Authorization": f"Bearer {FX_RATES_API_KEY}"})
        response.raise_for_status()
        fx_data = response.json()
        return fx_data['rates']
    except requests.RequestException as e:
        logger.error(f"Error fetching FX rates: {str(e)}")
        raise

def calculate_derivative_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate derivative metrics using numpy.
    
    Args:
        df (pd.DataFrame): Input DataFrame containing financial metrics.
    
    Returns:
        pd.DataFrame: DataFrame with additional calculated metrics.
    """
    df['arr'] = df['recurring_revenue'] * 4  # Assuming quarterly data
    df['recurring_percentage_revenue'] = df['recurring_revenue'] / df['total_revenue'] * 100
    df['revenue_per_fte'] = df['total_revenue'] / df['employees']
    df['gross_profit_per_fte'] = df['gross_profit'] / df['employees']
    df['change_in_cash'] = df['cash_balance'] - df['cash_balance'].shift(1)
    df['revenue_growth'] = (df['total_revenue'] - df['total_revenue'].shift(1)) / df['total_revenue'].shift(1) * 100
    df['monthly_cash_burn'] = -df['cash_burn'] / 3  # Assuming quarterly data
    df['runway_months'] = np.where(df['monthly_cash_burn'] > 0, df['cash_balance'] / df['monthly_cash_burn'], np.inf)
    
    # Additional metrics as per requirements
    df['sales_marketing_percentage_revenue'] = df['sales_marketing_expense'] / df['total_revenue'] * 100
    df['total_operating_percentage_revenue'] = df['total_operating_expense'] / df['total_revenue'] * 100
    df['gross_profit_margin'] = df['gross_profit'] / df['total_revenue'] * 100
    
    return df

@func.Function
def transform_data(input_data: Dict) -> Dict:
    """
    Performs data transformation tasks including currency conversion and calculation of derivative metrics.
    
    Args:
        input_data (Dict): Input financial metrics data.
    
    Returns:
        Dict: Transformed financial metrics including currency conversions and derivative calculations.
    """
    try:
        # Retrieve the latest foreign exchange rates
        fx_rates = get_fx_rates()
        
        # Load input financial metrics data using pandas
        df = pd.DataFrame([input_data])
        
        # Perform currency conversion
        base_currency = df['currency'].iloc[0]
        for currency in ['USD', 'CAD']:
            if currency != base_currency:
                conversion_rate = fx_rates[currency] / fx_rates[base_currency]
                for col in df.select_dtypes(include=[np.number]).columns:
                    df[f'{col}_{currency}'] = df[col] * conversion_rate
        
        # Calculate derivative metrics
        df = calculate_derivative_metrics(df)
        
        # Convert DataFrame back to dictionary
        transformed_data = df.to_dict(orient='records')[0]
        
        # Log successful transformation
        logger.info(f"Data transformation completed successfully for company_id: {transformed_data.get('company_id')}")
        
        return transformed_data
    except Exception as e:
        logger.error(f"Error in data transformation: {str(e)}")
        raise

# Timer trigger configuration
@func.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True)
def main(myTimer: func.TimerRequest, outputQueue: func.Out[str]) -> None:
    """
    Main function triggered every 5 minutes to perform data transformation tasks.
    
    Args:
        myTimer (func.TimerRequest): Timer trigger information.
        outputQueue (func.Out[str]): Output binding for the transformed data.
    """
    if myTimer.past_due:
        logger.info('The timer is past due!')
    
    logger.info('Python timer trigger function executed.')
    
    try:
        # In a real scenario, we would fetch the input data from a queue or database
        # For this example, we'll use a mock input
        mock_input = {
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
            "employees": 100,
        }
        
        transformed_data = transform_data(mock_input)
        
        # Store the transformed data in the specified output queue
        outputQueue.set(str(transformed_data))
        
        logger.info("Data transformation and queue storage completed successfully.")
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        # In a production environment, we might want to implement retry logic or alert mechanisms here

# HTTP trigger for manual execution or testing
@func.http_trigger(authLevel=func.AuthLevel.FUNCTION)
def manual_trigger(req: func.HttpRequest, outputQueue: func.Out[str]) -> func.HttpResponse:
    """
    HTTP trigger function for manual execution or testing of the data transformation process.
    
    Args:
        req (func.HttpRequest): The HTTP request object.
        outputQueue (func.Out[str]): Output binding for the transformed data.
    
    Returns:
        func.HttpResponse: HTTP response indicating the result of the operation.
    """
    logger.info('Manual trigger function processed a request.')
    
    try:
        req_body = req.get_json()
        transformed_data = transform_data(req_body)
        outputQueue.set(str(transformed_data))
        return func.HttpResponse("Data transformation completed successfully.", status_code=200)
    except ValueError:
        return func.HttpResponse("Invalid JSON input.", status_code=400)
    except Exception as e:
        logger.error(f"Error in manual trigger: {str(e)}")
        return func.HttpResponse("An error occurred during data transformation.", status_code=500)

if __name__ == "__main__":
    # This block is for local testing purposes
    mock_input = {
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
        "employees": 100,
    }
    result = transform_data(mock_input)
    print(result)