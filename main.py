from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie", version="1.0.0", description="Google Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class LearnRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html"
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QARequest):
    return {"answer": answer_question(payload.question)}


@app.post("/explain")
async def explain(payload: TextRequest):
    return {"explanation": explain_topic(payload.text)}


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    return {"quiz": generate_quiz(payload.text)}


@app.post("/summarize")
async def summarize(payload: TextRequest):
    return {"summary": summarize_text(payload.text)}


@app.post("/learn/recommendations")
async def learn(payload: LearnRequest):
    return {"recommendations": get_learning_recommendations(payload.topic, payload.level)}
