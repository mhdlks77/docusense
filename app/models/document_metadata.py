from pydantic import BaseModel
from datetime import datetime

class DocumentMetadata(BaseModel):
    filename: str
    filesize: int
    uploaded_at: datetime
    processed_text_path: str
    extracted_text_length: int
    
    