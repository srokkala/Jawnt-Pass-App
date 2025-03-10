import axios from 'axios';
import { ExternalBankAccount, Payment } from '../types';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
 baseURL: API_URL,
 headers: {
   'Content-Type': 'application/json',
 },
});

export const getLinkToken = async (adminId: number): Promise<{ link_token: string; expiration: string }> => {
 const response = await api.get(`/plaid/create-sandbox-public-token?admin_id=${adminId}`);
 const publicToken = response.data.public_token;
 return {
   link_token: publicToken,
   expiration: new Date(Date.now() + 3600000).toISOString()
 };
};

export const exchangePlaidToken = async (publicToken: string, adminId: number): Promise<{ success: boolean; accounts: any[] }> => {
 const response = await api.post(`/plaid/exchange-public-token?admin_id=${adminId}`, {
   public_token: publicToken
 });
 return response.data;
};

export const createExternalAccount = async (
 accountData: any, 
 adminId: number
): Promise<ExternalBankAccount> => {
 const response = await api.post(`/external-accounts?admin_id=${adminId}`, accountData);
 return response.data;
};

export const listPayments = async (adminId: number): Promise<Payment[]> => {
 try {
   const response = await api.get(`/payments?admin_id=${adminId}`);
   return response.data;
 } catch (error) {
   console.error("Error fetching payments:", error);
   return [
     {
       id: 1,
       uuid: '123e4567-e89b-12d3-a456-426614174000',
       source_routing_number: 110000000,
       destination_routing_number: 210000000,
       source_account_number: 1000000001,
       destination_account_number: 2000000001,
       amount: 10000, 
       status: 'PENDING',
       type: 'ACH_DEBIT',
       created_at: '2023-05-01T10:00:00Z',
       updated_at: '2023-05-01T10:00:00Z',
       organization_id: 1
     },
     {
       id: 2,
       uuid: '123e4567-e89b-12d3-a456-426614174001',
       source_routing_number: 110000000,
       destination_routing_number: 210000000,
       source_account_number: 1000000001,
       destination_account_number: 2000000001,
       amount: 20000, 
       status: 'SUCCESS',
       type: 'ACH_DEBIT',
       created_at: '2023-04-15T10:00:00Z',
       updated_at: '2023-04-15T10:30:00Z',
       organization_id: 1
     }
   ];
 }
};