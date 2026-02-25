from mcp.server.fastmcp import FastMCP
import re

# Initialize MCP Server
mcp = FastMCP("ClaimGuard-InsureTech")

# Mock OCR function (Replace with Azure/Tesseract later)
def perform_ocr(file_path: str) -> str:
    # In a real scenario, this would load the image/pdf and extract text
    return f"[MOCK OCR CONTENT from {file_path}] User ID: A123456789. Mobile: 0912-345-678. Email: user@example.com. Landline: 02-87654321. Diagnosis: Fracture."

@mcp.tool()
def process_claim_document(file_path: str, claim_id: str) -> dict:
    """
    Process a claim document: Run OCR, Redact PII, and return safe text.
    """
    print(f"Processing claim {claim_id} with file {file_path}")
    
    # 1. OCR
    raw_text = perform_ocr(file_path)
    
    # 2. PII Detection & Redaction
    # Taiwain ID Regex (Simplified)
    id_pattern = r"[A-Z][1-2]\d{8}"
    # Mobile: 09xx-xxx-xxx or 09xxxxxxxx
    mobile_pattern = r"09\d{2}-?\d{3}-?\d{3}"
    # Landline: 0x-xxxxxxx or 0xx-xxxxxxx (e.g., 02-12345678, 04-1234567)
    landline_pattern = r"0\d{1,2}-?\d{6,8}"
    # Email
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    
    redacted_text = raw_text
    pii_found = []

    # Helper to redact and track
    def redact(pattern, label, text):
        matches = re.findall(pattern, text)
        if matches:
            pii_found.extend(matches)
            return re.sub(pattern, label, text)
        return text

    redacted_text = redact(id_pattern, "[REDACTED_ID]", redacted_text)
    redacted_text = redact(mobile_pattern, "[REDACTED_MOBILE]", redacted_text)
    redacted_text = redact(landline_pattern, "[REDACTED_LANDLINE]", redacted_text)
    redacted_text = redact(email_pattern, "[REDACTED_EMAIL]", redacted_text)

    # 3. Fraud Check (Basic Logic)
    fraud_score = 0.0
    if "Fracture" in redacted_text and "Duplicate" in redacted_text:
        fraud_score = 0.8 # High risk

    return {
        "claim_id": claim_id,
        "original_length": len(raw_text),
        "safe_text": redacted_text,
        "pii_detected_count": len(pii_found),
        "fraud_risk_score": fraud_score
    }

if __name__ == "__main__":
    mcp.run()
