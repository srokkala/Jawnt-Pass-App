from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime

class SuperUser(BaseModel):
    id: int
    uid: uuid.UUID

class OrganizationAdministrator(BaseModel):
    id: int
    uid: uuid.UUID
    first_name: str
    last_name: str
    organization_id: int

class InternalOrganizationBankAccount(BaseModel):
    id: int
    uuid: uuid.UUID
    type: Literal["funding", "claims"]
    account_number: int
    routing_number: int

class ExternalOrganizationBankAccount(BaseModel):
    id: int
    uuid: uuid.UUID
    account_id: str  
    account_name: str
    account_type: str
    account_subtype: str
    routing_number: int
    account_number: int
    organization_id: int

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class PaymentType(str, Enum):
    ACH_DEBIT = "ACH_DEBIT"
    ACH_CREDIT = "ACH_CREDIT"
    
class Payment(BaseModel):
    id: int
    uuid: uuid.UUID
    source_routing_number: int
    destination_routing_number: int
    source_account_number: int
    destination_account_number: int
    amount: int
    status: str
    type: str
    created_at: datetime
    updated_at: datetime
    idempotency_key: str
    organization_id: int

class ExternalAccountCreate(BaseModel):
    account_id: str
    account_name: str
    account_type: str
    account_subtype: str
    routing_number: int
    account_number: int

class InternalAccountCreate(BaseModel):
    type: Literal["funding", "claims"]
    account_number: int
    routing_number: int

class InternalAccountUpdate(BaseModel):
    type: Optional[Literal["funding", "claims"]] = None

class PaymentCreate(BaseModel):
    internal_account_id: int
    external_account_id: int
    amount: int