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
    
    #We are only accepting pdf for now
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save pdf to the uploads folder (cloud later)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Extract text
    extracted_text = extract_text_pdf(file_path)
    
    # Save extracted text in "processed" folder
    processed_path = os.path.join("processed", file.filename.replace(".pdf", ".txt"))
    os.makedirs("processed", exist_ok=True)
    
        
    with open(processed_path, "w", encoding="utf-8") as out:
        out.write(extracted_text)
    
    # Build metadata object
    metadata = DocumentMetadata(
        filename=file.filename,
        filesize= os.path.getsize(file_path),
        uploaded_at= datetime.now(),
        processed_text_path= processed_path,
        extracted_text_length= len(extracted_text)
    )
    
    # save metadata to JSON
    existing = load_metadata()
    existing.append(metadata.model_dump())
    save_metadata(existing)

    return {
        "status": "uploaded and processed",
        "metadata": metadata.model_dump(),
        "preview": extracted_text[:200]
    }
