from fastapi import UploadFile, File,FastAPI
import shutil
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import QuestionRequest
from app.rag import ask_pdf, process_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/ask")
def ask_question(request: QuestionRequest):
    answer = ask_pdf(request.question)
    return {
        "answer": answer
    }


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed."
        }

    path = f"{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_pdf(path)

    return {
        "message": "PDF uploaded successfully."
    }