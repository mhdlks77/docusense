from fastapi import FastAPI, UploadFile, File
import shutil
import os
from app.file_handlers.pdf_handler import extract_text_pdf

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Docusense backend running"}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    
    #We are only accepting pdf for now
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Extract text
    extracted_text = extract_text_pdf(file_path)
    
    # Save extracted text in "processed" folder
    processed_path = os.path.join("processed", file.filename.replace(".pdf", ".txt"))
    os.makedirs("processed", exist_ok=True)
    
    with open(processed_path, "w", encoding="utf-8") as out:
        out.write(extracted_text)

    return {
        "filename": file.filename,
        "status": "uploaded and processed",
        "pdf_saved_to": file_path,
        "text_saved_to": processed_path,
        "extracted_text_preview": extracted_text[:300]  # small preview
    }
