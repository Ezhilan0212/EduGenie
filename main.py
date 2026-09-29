from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from models import (
    QARequest, TextRequest, QuizRequest, LearningPathRequest,
    QAResponse, TextResponse, QuizResponse, LearningPathResponse, ErrorResponse
)
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": settings.gemini_configured,
        "model": settings.gemini_model,
        "local_explanation_enabled": settings.enable_local_explanation,
    }


@app.post("/qa", response_model=QAResponse, responses={500: {"model": ErrorResponse}})
async def qa(payload: QARequest):
    try:
        return QAResponse(answer=await answer_question(payload.question))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/explain", response_model=TextResponse, responses={500: {"model": ErrorResponse}})
async def explain(payload: TextRequest):
    try:
        return TextResponse(result=await explain_concept(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/quiz", response_model=QuizResponse, responses={500: {"model": ErrorResponse}})
async def quiz(payload: QuizRequest):
    try:
        return QuizResponse(questions=await generate_quiz(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/summarize", response_model=TextResponse, responses={500: {"model": ErrorResponse}})
async def summarize(payload: TextRequest):
    try:
        return TextResponse(result=await summarize_text(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
    responses={500: {"model": ErrorResponse}},
)
async def learning_path(payload: LearningPathRequest):
    try:
        return LearningPathResponse(
            result=await get_learning_recommendations(payload.topic, payload.level)
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
