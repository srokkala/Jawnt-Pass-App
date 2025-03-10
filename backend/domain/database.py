from typing import Dict, List, Optional, Generic, TypeVar, Any
import uuid
from datetime import datetime
from domain.models import SuperUser, OrganizationAdministrator, InternalOrganizationBankAccount, ExternalOrganizationBankAccount, Payment

T = TypeVar('T')

class InMemoryTable(Generic[T]):
    """Generic in-memory table implementation using a hashmap data structure"""
    
    def __init__(self):
        self.data: Dict[int, Dict[str, Any]] = {}
        self.next_id = 1
    
    def create(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item in the table"""
        item_id = self.next_id
        item['id'] = item_id
        if 'uuid' not in item:
            item['uuid'] = uuid.uuid4()
        self.data[item_id] = item
        self.next_id += 1
        return item
    
    def get(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get an item by ID"""
        return self.data.get(item_id)
    
    def list(self) -> List[Dict[str, Any]]:
        """List all items in the table"""
        return list(self.data.values())
    
    def update(self, item_id: int, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an item by ID"""
        if item_id not in self.data:
            return None
        
        current_item = self.data[item_id]
        for key, value in item.items():
            if key != 'id' and key != 'uuid':  
                current_item[key] = value
                
        return current_item
    
    def delete(self, item_id: int) -> bool:
        """Delete an item by ID"""
        if item_id not in self.data:
            return False
        del self.data[item_id]
        return True
    
    def filter(self, **kwargs) -> List[Dict[str, Any]]:
        """Filter items by attributes"""
        result = []
        for item in self.data.values():
            match = True
            for key, value in kwargs.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                result.append(item)
        return result

class Database:
    """In-memory database with tables for all entities"""
    
    def __init__(self):
        self.super_users = InMemoryTable[SuperUser]()
        self.organization_administrators = InMemoryTable[OrganizationAdministrator]()
        self.internal_accounts = InMemoryTable[InternalOrganizationBankAccount]()
        self.external_accounts = InMemoryTable[ExternalOrganizationBankAccount]()
        self.payments = InMemoryTable[Payment]()
        
        self._add_test_data()
    
    def _add_test_data(self):
        self.super_users.create({
            "uid": uuid.uuid4()
        })
        
        self.organization_administrators.create({
            "uid": uuid.uuid4(),
            "first_name": "Steven",
            "last_name": "Rokkala",
            "organization_id": 1
        })
        
        internal_account = self.internal_accounts.create({
            "uuid": uuid.uuid4(),
            "type": "funding",
            "account_number": 2000000001,
            "routing_number": 210000000
        })
        
        external_account = self.external_accounts.create({
            "uuid": uuid.uuid4(),
            "account_id": "plaid-sandbox-account-123",
            "account_name": "Plaid Checking",
            "account_type": "depository",
            "account_subtype": "checking",
            "routing_number": 110000000,
            "account_number": 1000000001,
            "organization_id": 1
        })
        
        now = datetime.now()
        
        self.payments.create({
            "uuid": uuid.uuid4(),
            "source_routing_number": external_account["routing_number"],
            "destination_routing_number": internal_account["routing_number"],
            "source_account_number": external_account["account_number"],
            "destination_account_number": internal_account["account_number"],
            "amount": 10000,  
            "status": "PENDING",
            "type": "ACH_DEBIT",
            "created_at": now,
            "updated_at": now,
            "idempotency_key": str(uuid.uuid4()),
            "organization_id": 1
        })
        
        self.payments.create({
            "uuid": uuid.uuid4(),
            "source_routing_number": external_account["routing_number"],
            "destination_routing_number": internal_account["routing_number"],
            "source_account_number": external_account["account_number"],
            "destination_account_number": internal_account["account_number"],
            "amount": 20000,  
            "status": "SUCCESS",
            "type": "ACH_DEBIT",
            "created_at": now,
            "updated_at": now,
            "idempotency_key": str(uuid.uuid4()),
            "organization_id": 1
        })
        
        self.payments.create({
            "uuid": uuid.uuid4(),
            "source_routing_number": external_account["routing_number"],
            "destination_routing_number": internal_account["routing_number"],
            "source_account_number": external_account["account_number"],
            "destination_account_number": internal_account["account_number"],
            "amount": 5000,  
            "status": "FAILURE",
            "type": "ACH_DEBIT",
            "created_at": now,
            "updated_at": now,
            "idempotency_key": str(uuid.uuid4()),
            "organization_id": 1
        })

db = Database()