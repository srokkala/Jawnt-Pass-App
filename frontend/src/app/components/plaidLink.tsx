'use client';

import { useState, useCallback } from 'react';
import { getLinkToken, exchangePlaidToken, createExternalAccount } from '../services/api';
import { ExternalBankAccount } from '../types';

interface PlaidLinkProps {
  adminId: number;
  onSuccess: (account: ExternalBankAccount) => void;
  buttonText?: string;
}

export default function PlaidLink({ adminId, onSuccess, buttonText = 'Connect Bank Account' }: PlaidLinkProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleClick = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const tokenData = await getLinkToken(adminId);
      console.log("Got public token:", tokenData);

      const exchangeData = await exchangePlaidToken(tokenData.link_token, adminId);
      console.log("Exchange data:", exchangeData);

      if (exchangeData.success && exchangeData.accounts && exchangeData.accounts.length > 0) {
        const account = exchangeData.accounts[0];
        
        const accountData = {
          account_id: account.account_id,
          account_name: account.name || "Plaid Account",
          account_type: account.type || "depository",
          account_subtype: account.subtype || '',
          routing_number: typeof account.routing_number === 'string' 
            ? parseInt(account.routing_number) 
            : account.routing_number || 110000000,
          account_number: typeof account.account_number === 'string' 
            ? parseInt(account.account_number) 
            : account.account_number || 1000000000,
        };

        console.log("Creating external account with data:", accountData);
        const newAccount = await createExternalAccount(accountData, adminId);
        onSuccess(newAccount);
      } else {
        throw new Error("No accounts returned from exchange");
      }
    } catch (error) {
      console.error("Error connecting bank account:", error);
      setError(error instanceof Error ? error.message : "Failed to connect bank account");
    } finally {
      setIsLoading(false);
    }
  }, [adminId, onSuccess]);

  return (
    <div>
      <button
        onClick={handleClick}
        disabled={isLoading}
        className="plaid-button bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-blue-300"
      >
        {isLoading ? "Connecting..." : buttonText}
      </button>
      {error && <p className="text-red-600 mt-2">{error}</p>}
    </div>
  );
}