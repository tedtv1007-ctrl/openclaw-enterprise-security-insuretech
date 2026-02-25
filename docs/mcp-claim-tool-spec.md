# MCP Claim Tool Specification (InsureTech)

## Overview
An MCP (Model Context Protocol) tool enabling AI agents to interact with the insurance claims process securely.

## Capabilities
1.  **OCR Processing**: Extract text from uploaded claim documents (PDF/Images).
2.  **PII Redaction**: Automatically detect and mask sensitive data before LLM processing.
3.  **Fraud Detection Signal**: Basic rule-based check for duplicate claims or suspicious patterns.

## API Schema (Draft)

### `process_claim_document`
-   **Input**: `file_path` (string), `claim_id` (string)
-   **Output**: `masked_text` (string), `pii_detected` (list[string]), `fraud_score` (0-1 float)
-   **Logic**:
    1.  Load file.
    2.  Run OCR (Tesseract / Azure Form Recognizer).
    3.  Regex scan for IDs (`[A-Z][1-2]\d{8}`), Phone numbers.
    4.  Replace detected PII with `[REDACTED_ID]`.
    5.  Return safe text.

## Security Constraints
-   Images/PDFs are processed in-memory or ephemeral storage only.
-   No unmasked PII is ever sent to the LLM context.
-   Audit log entry created for every execution.
