from fastapi import FastAPI, UploadFile, File
import shutil
import os
from datetime import datetime
from app.models.document_metadata import DocumentMetadata
from app.storage.metadata_store import load_metadata, save_metadata

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Docusense backend running"}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save pdf to the uploads folder (cloud later)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "status": "uploaded",
        "path": file_path
    }
