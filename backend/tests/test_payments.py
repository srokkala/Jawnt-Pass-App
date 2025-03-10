import unittest
from unittest.mock import patch, Mock
import uuid
from domain.models import PaymentStatus
from lib.jawnt.client import perform_ach_debit, PaymentResponse

class TestPayments(unittest.TestCase):
    @patch("lib.jawnt.client.external_call")
    def test_perform_ach_debit(self, mock_external_call):
        payment_id = uuid.uuid4()
        mock_external_call.return_value = PaymentResponse(
            payment_id=payment_id,
            status=PaymentStatus.PENDING,
            amount=5000,
        )
        
        response = perform_ach_debit(
            "internal_account_id",
            "external_account_id",
            5000,
            "idempotency_key",
        )
        
        self.assertEqual(response.status, PaymentStatus.PENDING)
        self.assertEqual(response.amount, 5000)

    @patch("lib.jawnt.client.external_call")
    def test_perform_ach_debit_with_specific_amount(self, mock_external_call):
        payment_id = uuid.uuid4()
        test_amount = 10000  
        mock_external_call.return_value = PaymentResponse(
            payment_id=payment_id,
            status=PaymentStatus.PENDING,
            amount=test_amount,
        )
        
        response = perform_ach_debit(
            "internal_account_id",
            "external_account_id",
            test_amount,
            "idempotency_key",
        )
        
        mock_external_call.assert_called_once()
        self.assertEqual(response.amount, test_amount)
        self.assertEqual(response.status, PaymentStatus.PENDING)

if __name__ == '__main__':
    unittest.main()