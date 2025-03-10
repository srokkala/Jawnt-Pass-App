import time
from enum import Enum
from unittest.mock import patch
import uuid
from random import randint

class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class PaymentResponse:
    """
    Represents the response from an external payment service
    Amount is in cents
    """
    def __init__(self, payment_id, status, amount):
        self.payment_id = payment_id
        self.status = status
        self.amount = amount

def external_call(*args, amount) -> PaymentResponse:  # pylint: disable=unused-argument
    time.sleep(2)
    return PaymentResponse(
        payment_id=uuid.uuid4(),
        status=PaymentStatus.PENDING,
        amount=amount,
    )

def long_external_call() -> None:
    time.sleep(30)

def perform_ach_debit(
    internal_account_id: str,
    external_account_id: str,
    amount: int,
    idempotency_key: str,
) -> PaymentResponse:
    """
    Amount represents the amount in cents
    e.g $50.00 = 5000
    """
    return external_call(
        internal_account_id,
        external_account_id,
        idempotency_key,
        amount=amount,
    )

def perform_ach_credit(
    internal_account_id: str,
    external_account_id: str,
    amount: int,
    idempotency_key: str,
) -> PaymentResponse:
    """
    Amount represents the amount in cents
    e.g $50.00 = 5000
    """
    return external_call(
        internal_account_id,
        external_account_id,
        idempotency_key,
        amount=amount,
    )

def perform_book_payment(
    internal_account_id: str,
    external_account_id: str,
    amount: int,
    idempotency_key: str,
) -> PaymentResponse:
    """
    Amount represents the amount in cents
    e.g $50.00 = 5000
    """
    return external_call(
        internal_account_id,
        external_account_id,
        idempotency_key,
        amount=amount,
    )

def get_payment_status(
    payment_id: str,  # pylint: disable=unused-argument
) -> PaymentStatus:
    long_external_call()
    return (
        PaymentStatus.SUCCESS if randint(1, 2) == 1 else PaymentStatus.FAILURE
    )