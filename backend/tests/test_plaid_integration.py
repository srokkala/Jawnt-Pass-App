import unittest
from fastapi.testclient import TestClient
from api.main import app

class TestPlaidIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_sandbox_public_token(self):
        response = self.client.get("/api/plaid/create-sandbox-public-token?admin_id=1")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('public_token', response.json())

    def test_exchange_public_token(self):
        token_response = self.client.get("/api/plaid/create-sandbox-public-token?admin_id=1")
        public_token = token_response.json()['public_token']
        
        exchange_response = self.client.post(
            "/api/plaid/exchange-public-token?admin_id=1", 
            json={"public_token": public_token}
        )
        
        self.assertEqual(exchange_response.status_code, 200)
        self.assertIn('accounts', exchange_response.json())

if __name__ == '__main__':
    unittest.main()