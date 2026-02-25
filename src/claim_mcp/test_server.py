import unittest
from unittest.mock import patch
from server import process_claim_document

class TestClaimServer(unittest.TestCase):

    @patch('server.perform_ocr')
    def test_pii_redaction(self, mock_ocr):
        # Arrange
        mock_ocr.return_value = (
            "Patient: John Doe. "
            "ID: A123456789. "
            "Mobile: 0912-345-678. "
            "Landline: 02-87654321. "
            "Email: john.doe@example.com. "
            "DOB: 1990/01/01. "
            "Address: 台北市信義區信義路五段7號. "
            "Diagnosis: Fracture."
        )
        
        # Act
        result = process_claim_document("dummy_path.pdf", "CLM-001")
        
        # Assert
        safe_text = result['safe_text']
        
        # Verify redactions
        self.assertNotIn("A123456789", safe_text)
        self.assertIn("[REDACTED_ID]", safe_text)
        
        self.assertNotIn("0912-345-678", safe_text)
        self.assertIn("[REDACTED_MOBILE]", safe_text)
        
        self.assertNotIn("02-87654321", safe_text)
        self.assertIn("[REDACTED_LANDLINE]", safe_text)
        
        self.assertNotIn("john.doe@example.com", safe_text)
        self.assertIn("[REDACTED_EMAIL]", safe_text)

        self.assertNotIn("1990/01/01", safe_text)
        self.assertIn("[REDACTED_DOB]", safe_text)

        self.assertNotIn("台北市信義區信義路五段7號", safe_text)
        self.assertIn("[REDACTED_ADDRESS]", safe_text)
        
        # Verify non-PII remains
        self.assertIn("Patient: John Doe.", safe_text)
        self.assertIn("Diagnosis: Fracture.", safe_text)

    @patch('server.perform_ocr')
    def test_fraud_check(self, mock_ocr):
        # Arrange
        mock_ocr.return_value = "Diagnosis: Fracture. Note: Duplicate claim detected."
        
        # Act
        result = process_claim_document("dummy_path.pdf", "CLM-002")
        
        # Assert
        self.assertEqual(result['fraud_risk_score'], 0.8)

if __name__ == "__main__":
    unittest.main()
