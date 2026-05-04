
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Response, status
import os
import uuid 
from http import HTTPStatus
from pydantic import BaseModel
import tasks.celery_task as celeryTask
from tasks.celery_app import celery_app
from celery.result import AsyncResult

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

class TaskStatus(BaseModel):
    task_id: str
    status: str
    result: str | None
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

@app.post("/generate-prd")
async def generate_prd(input : PRDInput):
    task = celeryTask.generate_prd.delay(input.requirement, input.platform)
    return {"task_id": task.id}

@app.post("/detail-prd")
async def detail_prd(input : DetailPRDInput):
    task = celeryTask.detail_prd.delay(input.prd_content)
    return {"task_id": task.id}
    

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task = celeryTask.research.AsyncResult(task_id)
    if task.state == "PENDING":
        return {"status": "PENDING"}
    elif task.state == "STARTED":
        return {"status": "STARTED", "result": task.info}
    elif task.state == "SUCCESS":
        return {"status": "SUCCESS", "result": task.info}
    elif task.state == "FAILURE":
        return {"status": "FAILURE", "result": str(task.info)}

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