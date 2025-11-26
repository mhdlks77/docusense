import pdfplumber


def extract_text_pdf(filepath: str) -> str:
    
    # Here we will extract text from pdf using pdfplumber
    # another option is PyPDF2
    
    text = ""
    
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text() or ""
                text += extracted + "\n"
        if text.strip():
            return text
    except Exception as e:
        print("pdfplumber failed", e)
