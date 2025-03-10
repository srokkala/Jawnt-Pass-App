import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.main import app

class TestExternalAccounts(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_external_account(self):
        account_data = {
            "account_id": "test_account_1",
            "account_name": "Test Checking",
            "account_type": "CHECKING",
            "account_subtype": "PERSONAL",
            "routing_number": "123456789",
            "account_number": "9876543210"
        }
        
        response = self.client.post("/api/external-accounts?admin_id=1", json=account_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['account_id'], account_data['account_id'])

    def test_list_payments(self):
        response = self.client.get("/api/payments?admin_id=1")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))

if __name__ == '__main__':
    unittest.main()