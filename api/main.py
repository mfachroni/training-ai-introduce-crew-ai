
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Response, status
import os
import uuid 
from http import HTTPStatus
from pydantic import BaseModel
import tasks.celery_task as celeryTask
from tasks.celery_app import celery_app
from celery.result import AsyncResult

TEXT_FOLDER = 'files/text/'

os.makedirs(TEXT_FOLDER, exist_ok=True)

class ResearchInput(BaseModel):
    topic: str
    language: str = "English"

class MarketAnalysisInput(BaseModel):
    topic: str
    year: str | None = None
    location: str = "Global"

class PRDInput(BaseModel):
    requirement: str
    platform: str

class DetailPRDInput(BaseModel):
    prd_content: str

class TechnicalDocInput(BaseModel):
    prd_content: str
    tech_stack: str

class RequirementInput(BaseModel):
    requirement: str
    target_audience: str

class TaskStatus(BaseModel):
    task_id: str
    status: str
    result: str | None | dict 
    error: str | None

app = FastAPI()

@app.post("/research")
async def research(input : ResearchInput):
    task = celeryTask.research.delay(input.topic, input.language)
    return {"task_id": task.id}

@app.post("/analyze-market")
async def analyze_market(input : MarketAnalysisInput):
    task = celeryTask.analyze_market.delay(input.topic, input.year, input.location)
    return {"task_id": task.id}

@app.post("/generate-technical-doc")
async def generate_technical_doc(input : TechnicalDocInput):
    task = celeryTask.generate_technical_doc.delay(input.prd_content, input.tech_stack)
    return {"task_id": task.id}

@app.post("/gather-requirements")
async def gather_requirements(input : RequirementInput):
    task = celeryTask.gather_requirements.delay(input.requirement, input.target_audience)
    return {"task_id": task.id}

# @app.post("/detail-prd")
# async def detail_prd(input : DetailPRDInput):
#     task = celeryTask.detail_prd.delay(input.prd_content)
#     return {"task_id": task.id}
    

@app.get('/status/{task_id}', response_model=TaskStatus)
async def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id" : task_id,
        "status" : task_result.state,
        "result" : None,
        "error" : None
    }

    if task_result.state == "SUCCESS":
        response['result'] = task_result.result
    elif task_result.state == "FAILURE":
        response['error'] = str(task_result.info)

    return response

#========================= DAY 2 =============================

@app.post("/text-analyzer")
async def file_text_analyzer(file: UploadFile = File(...)):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

    file_extension = os.path.splitext(file.filename)[1]

    if file_extension != ".txt":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

    unique_filename = str(uuid.uuid4()) + file_extension
    file_loc = os.path.join(TEXT_FOLDER, unique_filename)

    content = await file.read()

    with open(file_loc, "wb") as f:
        f.write(content)

    task = celeryTask.file_text_analyzer.delay(file_loc)
    return {"task_id": task.id, "file_location": file_loc, "content" : content}
