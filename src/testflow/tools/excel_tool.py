from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pandas as pd

class ExcelAnalyzerInput(BaseModel):
    """Input schema for ExcelAnalyzerTool."""
    file_path: str = Field(..., description="The path to the Excel file (.xlsx) to analyze.")

class ExcelAnalyzerTool(BaseTool):
    name: str = "Excel Analyzer"
    description: str = "Reads and analyzes Excel files (.xlsx), converting them to a readable string format for data analysis."
    args_schema: Type[BaseModel] = ExcelAnalyzerInput

    def _run(self, file_path: str) -> str:
        try:
            # Read all sheets to give a complete picture
            xl = pd.ExcelFile(file_path)
            full_content = []
            for sheet_name in xl.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                # Take a sample or head if it's too large, but for now just convert to string
                # Adding sheet info
                content = f"Sheet: {sheet_name}\n"
                content += df.to_string(index=False)
                full_content.append(content)
            
            return "\n\n".join(full_content)
        except Exception as e:
            return f"Error reading Excel file: {str(e)}"
