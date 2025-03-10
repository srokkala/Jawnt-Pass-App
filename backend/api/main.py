from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
import os 
import certifi

from datetime import datetime

from domain.models import (
    SuperUser, OrganizationAdministrator, InternalOrganizationBankAccount, 
    ExternalOrganizationBankAccount, Payment, PaymentStatus, PaymentType,
    ExternalAccountCreate, InternalAccountCreate, InternalAccountUpdate, PaymentCreate
)
from domain.database import db
from message_queue.queue import message_queue
from lib.jawnt.client import perform_ach_debit, get_payment_status as client_get_payment_status
from lib.jawnt.client import PaymentStatus as ClientPaymentStatus

import plaid
from plaid.api import plaid_api
from plaid.configuration import Configuration  
from plaid.api_client import ApiClient  
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.auth_get_request import AuthGetRequest

# Plaid credentials from environment variables (with sandbox fallback values)

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID', '6758563294bbe4001b5c5279')
PLAID_SECRET = os.getenv('PLAID_SECRET', '386a94d4b632d57fe91b7b0f8506b3')

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class PublicTokenRequest(BaseModel):
    public_token: str

# Map client payment status to our model payment status
def map_client_status_to_model(client_status: ClientPaymentStatus) -> PaymentStatus:
    status_mapping = {
        ClientPaymentStatus.PENDING: PaymentStatus.PENDING,
        ClientPaymentStatus.SUCCESS: PaymentStatus.SUCCESS,
        ClientPaymentStatus.FAILURE: PaymentStatus.FAILURE
    }
    return status_mapping.get(client_status, PaymentStatus.PENDING)

# Dependency for getting the current organization administrator
async def get_current_admin(admin_id: int = Query(...)) -> OrganizationAdministrator:
    admin_data = db.organization_administrators.get(admin_id)
    if not admin_data:
        raise HTTPException(status_code=404, detail="Administrator not found")
    return OrganizationAdministrator(**admin_data)


configuration = Configuration(
    host='https://sandbox.plaid.com',
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    },
    ssl_ca_cert=certifi.where()
)

api_client = plaid_api.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)



# Dependency for getting the current superuser
async def get_current_superuser(user_id: int = Query(...)) -> SuperUser:
    user_data = db.super_users.get(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="Superuser not found")
    return SuperUser(**user_data)

@app.get("/api/plaid/create-sandbox-public-token")
async def create_sandbox_public_token(admin_id: int):
    try:
       
        institution_id = "ins_3"  

        request = SandboxPublicTokenCreateRequest(
            institution_id=institution_id,
            initial_products=[Products("auth"), Products("transactions")]
        )
        
        print(f"Creating sandbox token for institution: {institution_id}")
        
        response = client.sandbox_public_token_create(request)
        
        
        public_token = response.public_token
        
        print(f"Created public token: {public_token}")
        return {"public_token": public_token}
    
    except Exception as e:
        print(f"Error creating sandbox public token: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create public token: {str(e)}")
        

        
@app.post("/api/plaid/exchange-public-token")  
async def exchange_public_token(request: PublicTokenRequest, admin_id: int):
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=request.public_token
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response.access_token
        
        print("Exchanged public token for access token")

        accounts_request = AccountsGetRequest(access_token=access_token)
        accounts_response = client.accounts_get(accounts_request)
        
        # Try to get auth data for account/routing numbers
        try:
            auth_request = AuthGetRequest(access_token=access_token)
            auth_response = client.auth_get(auth_request)
            
            accounts_with_numbers = []
            for account in accounts_response.accounts:
                account_id = account.account_id
                # Find matching account in auth_response
                for auth_account in auth_response.numbers.ach:
                    if auth_account.account_id == account_id:
                        account_with_numbers = account.to_dict()
                        account_with_numbers['account_number'] = auth_account.account
                        account_with_numbers['routing_number'] = auth_account.routing
                        accounts_with_numbers.append(account_with_numbers)
                        break
        
            
            return {
                "success": True, 
                "accounts": accounts_with_numbers
            }
            
        except Exception as auth_error:
            print(f"Error getting auth data: {str(auth_error)}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": True,
                "accounts": accounts_with_numbers,
                "error": "Auth data not available"
            }

    except Exception as e:
        print(f"Error exchanging public token: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to exchange public token: {str(e)}")
    
    

# External Bank Account Routes (for Organization Administrators)
@app.post("/api/external-accounts", response_model=ExternalOrganizationBankAccount)
async def create_external_account(
    account_data: ExternalAccountCreate,
    admin: OrganizationAdministrator = Depends(get_current_admin)
):
    account_dict = {
        "uuid": uuid.uuid4(),
        "account_id": account_data.account_id,
        "account_name": account_data.account_name,
        "account_type": account_data.account_type,
        "account_subtype": account_data.account_subtype,
        "routing_number": account_data.routing_number,
        "account_number": account_data.account_number,
        "organization_id": admin.organization_id
    }
    
    created_account_data = db.external_accounts.create(account_dict)
    return ExternalOrganizationBankAccount(**created_account_data)

@app.get("/api/payments", response_model=List[Payment])
async def list_payments(
    admin: OrganizationAdministrator = Depends(get_current_admin)
):
    payment_data_list = db.payments.filter(organization_id=admin.organization_id)
    return [Payment(**payment_data) for payment_data in payment_data_list]

# Internal Bank Account Routes (for Superusers)
@app.post("/api/internal-accounts", response_model=InternalOrganizationBankAccount)
async def create_internal_account(
    account_data: InternalAccountCreate,
    superuser: SuperUser = Depends(get_current_superuser)
):
    account_dict = {
        "uuid": uuid.uuid4(),
        "type": account_data.type,
        "account_number": account_data.account_number,
        "routing_number": account_data.routing_number
    }
    
    created_account_data = db.internal_accounts.create(account_dict)
    return InternalOrganizationBankAccount(**created_account_data)

@app.patch("/api/internal-accounts/{account_id}", response_model=InternalOrganizationBankAccount)
async def update_internal_account(
    account_id: int,
    account_data: InternalAccountUpdate,
    superuser: SuperUser = Depends(get_current_superuser)
):
    update_data = {}
    if account_data.type is not None:
        update_data["type"] = account_data.type
    
    updated_data = db.internal_accounts.update(account_id, update_data)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Internal account not found")
    
    return InternalOrganizationBankAccount(**updated_data)

@app.delete("/api/internal-accounts/{account_id}")
async def delete_internal_account(
    account_id: int,
    superuser: SuperUser = Depends(get_current_superuser)
):
    deleted = db.internal_accounts.delete(account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Internal account not found")
    
    return {"success": True}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)