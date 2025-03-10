import unittest
from fastapi.testclient import TestClient
from api.main import app

class TestInternalAccounts(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_internal_account(self):
        account_data = {
            "type": "funding",
            "account_number": "1234567890",
            "routing_number": "987654321"
        }
        
        response = self.client.post("/api/internal-accounts?user_id=1", json=account_data)
        
        self.assertEqual(response.status_code, 200, f"Response body: {response.text}")
        self.assertEqual(response.json()['type'], account_data['type'])
        self.assertIn('id', response.json())

    def test_update_internal_account(self):
        create_data = {
            "type": "funding",
            "account_number": "1234567890",
            "routing_number": "987654321"
        }
        create_response = self.client.post("/api/internal-accounts?user_id=1", json=create_data)
        created_account_id = create_response.json()['id']

        update_data = {"type": "claims"}
        
        response = self.client.patch(f"/api/internal-accounts/{created_account_id}?user_id=1", json=update_data)
        
        self.assertEqual(response.status_code, 200, f"Response body: {response.text}")
        self.assertEqual(response.json()['type'], update_data['type'])

    def test_delete_internal_account(self):
        create_data = {
            "type": "funding",
            "account_number": "1234567890",
            "routing_number": "987654321"
        }
        create_response = self.client.post("/api/internal-accounts?user_id=1", json=create_data)
        created_account_id = create_response.json()['id']

        response = self.client.delete(f"/api/internal-accounts/{created_account_id}?user_id=1")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

if __name__ == '__main__':
    unittest.main()