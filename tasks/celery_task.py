from testflow.crews.prophet_crew.prophet_crew import ProphetCrew
from testflow.crews.crewanomali.crewanomali import Crewanomali
from testflow.crews.file_analyzer.file_analyzer import FileAnalyzer
from testflow.crews.content_crew.content_crew import ContentCrew
from testflow.crews.marketanalisator.marketanalisator import Marketanalisator
from testflow.crews.developer_crew.developer_crew import DeveloperCrew
from testflow.crews.spec_detailer_crew.spec_detailer_crew import SpecDetailerCrew
from testflow.crews.business_analysis_crew.business_analysis_crew import BusinessAnalysisCrew
from uvicorn import logging
from tasks.celery_app import celery_app
import logging
import traceback

from datetime import datetime

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, name="research")
def research(self, topic: str, language: str):
    self.update_state(state="RUNNING", meta={"message": "Starting research", "topic" : topic, "language": language})
    try:
        result = ContentCrew().crew().kickoff(inputs={
            "topic" : topic, 
            "language": language,
            "current_year": str(datetime.now().year)
        })
        return str(result)
    except Exception as exc:
        logger.error(f"Error: {exc} \n {traceback.format_exc()}")
        raise

@celery_app.task(bind=True, max_retries=3, name="analyze_market")
def analyze_market(self, topic: str, year: str | None = None, location: str = "Global"):
    self.update_state(state="RUNNING", meta={"message": "Starting market analysis", "topic" : topic, "year": year, "location": location})
    try:
        current_year = year if year else str(datetime.now().year)
        result = Marketanalisator().crew().kickoff(inputs={
            "topic" : topic,
            "location": location,
            "current_year": current_year
        })
        return str(result)
    except Exception as exc:
        logger.error(f"Error: {exc} \n {traceback.format_exc()}")
        raise

@celery_app.task(bind=True, max_retries=3, name="generate_technical_doc")
def generate_technical_doc(self, prd_content: str, tech_stack: str):
    self.update_state(state="RUNNING", meta={"message": "Generating detailed technical document", "prd_content_length" : len(prd_content), "tech_stack": tech_stack})
    try:
        result = DeveloperCrew().crew().kickoff(inputs={
            "prd_content" : prd_content,
            "tech_stack": tech_stack
        })
        return str(result)
    except Exception as exc:
        logger.error(f"Error: {exc} \n {traceback.format_exc()}")
        raise

@celery_app.task(bind=True, max_retries=3, name="gather_requirements")
def gather_requirements(self, requirement: str, target_audience: str):
    self.update_state(state="RUNNING", meta={"message": "Gathering requirements and business analysis", "requirement" : requirement, "target_audience": target_audience})
    try:
        result = BusinessAnalysisCrew().crew().kickoff(inputs={
            "requirement" : requirement,
            "target_audience": target_audience
        })
        return str(result)
    except Exception as exc:
        logger.error(f"Error: {exc} \n {traceback.format_exc()}")
        raise

@celery_app.task(bind=True, max_retries=3, name="detail_prd")
def detail_prd(self, prd_content: str):
    self.update_state(state="RUNNING", meta={"message": "Detailing PRD document", "prd_content_length" : len(prd_content)})
    try:
        result = SpecDetailerCrew().crew().kickoff(inputs={
            "prd_content" : prd_content
        })
        return str(result)
    except Exception as exc:
        logger.error(f"Error: {exc} \n {traceback.format_exc()}")
        raise



#============= Day 2 ====================

@celery_app.task(bind=True, max_retries=3, name="file_text_analyzer")
def file_text_analyzer(self, file: str):
    self.update_state(state="RUNNING", meta={"message": "Analyzing file", "file": file})
    try:
        result = FileAnalyzer().crew().kickoff(inputs={
            "file": file
        })
        return result.to_dict()
    except Exception as exc:
        logger.error(f"Error: {exc} \n {traceback.format_exc()}")
        raise

@celery_app.task(bind=True, max_retries=3, name="deteksi_anomali_excel")
def deteksi_anomali_excel(self, file: str):
    self.update_state(state="RUNNING", meta={"message": "Analyzing file", "file": file})
    try:
        result = Crewanomali().crew().kickoff(inputs={
            "file": file
        })
        return str(result)
    except Exception as exc:
        logger.error(f"Error: {exc} \n {traceback.format_exc()}")

@celery_app.task(bind=True, max_retries=3, name="forecasting_sales")
def forecasting_sales(self, file: str):
    self.update_state(state="RUNNING", meta={"message": "Performing time-series forecasting", "file": file})
    try:
        result = ProphetCrew().crew().kickoff(inputs={
            "file_path": file
        })
        return str(result)
    except Exception as exc:
        logger.error(f"Error: {exc} \n {traceback.format_exc()}")
        raise
        