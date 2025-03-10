export interface ExternalBankAccount {
    id: number;
    uuid: string;
    account_id: string;
    account_name: string;
    account_type: string;
    account_subtype: string;
    routing_number: number;
    account_number: number;
    organization_id: number;
  }
  
  export interface Payment {
    id: number;
    uuid: string;
    source_routing_number: number;
    destination_routing_number: number;
    source_account_number: number;
    destination_account_number: number;
    amount: number;
    status: string;
    type: string;
    created_at: string;
    updated_at: string;
    organization_id: number;
  }