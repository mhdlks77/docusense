from fastapi import FastAPI, UploadFile, File
import shutil
import os

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

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "status": "uploaded",
        "path": file_path
    }
