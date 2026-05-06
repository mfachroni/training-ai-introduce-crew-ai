from typing import Type
from pydantic import BaseModel, Field 
from crewai.tools import BaseTool 
import pandas as pd 
from prophet import Prophet
import os

class ToolProphetInput(BaseModel):
    file_path: str = Field(..., description="The path to the Excel file containing time-series data.")
    target_column: str = Field("sales", description="The column name to predict.")
    date_column: str = Field("date", description="The column name containing dates.")
    periods: int = Field(30, description="Number of days to forecast into the future.")

class ToolProphet(BaseTool):
    name: str = "Tool Prophet"
    description: str = "A tool to perform time-series forecasting using Facebook Prophet. It reads an Excel file and returns the predicted trends."
    args_schema: Type[BaseModel] = ToolProphetInput
    
    def _run(self, file_path: str, target_column: str = "sales", date_column: str = "date", periods: int = 30) -> str:
        try:
            if not os.path.exists(file_path):
                return f"Error: File not found at {file_path}"
            
            # Read Excel file
            df = pd.read_excel(file_path)
            
            if date_column not in df.columns or target_column not in df.columns:
                return f"Error: Columns '{date_column}' or '{target_column}' not found in file. Available columns: {list(df.columns)}"
            
            # Prepare data for Prophet
            # Prophet requires 'ds' for date and 'y' for value
            df_prophet = df[[date_column, target_column]].rename(columns={date_column: 'ds', target_column: 'y'})
            df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
            
            # Initialize and fit the model
            model = Prophet(yearly_seasonality=True, daily_seasonality=False, weekly_seasonality=True)
            model.fit(df_prophet)
            
            # Create future dataframe
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            
            # Extract relevant info from forecast
            # Last 'periods' rows are the forecast
            forecast_result = forecast.tail(periods)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            
            # Format results
            summary = f"Forecasting complete for {periods} days.\n"
            summary += "Summary of last 5 days forecasted:\n"
            summary += forecast_result.tail(5).to_string(index=False)
            
            # Calculate some metrics
            trend_direction = "UPWARD" if forecast['trend'].iloc[-1] > forecast['trend'].iloc[-periods] else "DOWNWARD"
            summary += f"\n\nOverall Trend Direction: {trend_direction}"
            
            return summary

        except Exception as e:
            return f"Error during forecasting: {str(e)}"