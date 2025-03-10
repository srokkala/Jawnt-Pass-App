'use client';

import { useState } from 'react';
import PlaidLink from '../components/plaidLink';
import PaymentList from '../components/paymentList';
import { ExternalBankAccount } from '../types';

export default function Dashboard() {
  // Hardcoding adminId to 1 but this would come from authentication if this wasn't a technical assessment
  const [adminId] = useState<number>(1);
  const [linkedAccounts, setLinkedAccounts] = useState<ExternalBankAccount[]>([]);
  
  const handleAccountLinked = (account: ExternalBankAccount) => {
    setLinkedAccounts(prev => [...prev, account]);
  };
  
  return (
    <div className="dashboard">
      <header className="header">
        <h1>Jawnt Banking Dashboard</h1>
        <p>Organization Administrator Portal</p>
      </header>
      
      <main className="dashboard-content">
        <h1 className="section-title">Integrations</h1>
        
        <div className="integration-card">
          <h2 className="integration-heading">Organization Funding Account</h2>
          
          <p className="integration-description">
            Jawnt uses Plaid to connect to your organization's bank account to automatically fund your members' passes each month.
          </p>
          
          {linkedAccounts.length === 0 ? (
            <PlaidLink 
              adminId={adminId} 
              onSuccess={handleAccountLinked} 
              buttonText="Connect Funding Account"
            />
          ) : (
            <div className="linked-accounts">
              {linkedAccounts.map((account) => (
                <div key={account.id} className="account-card">
                  <div className="account-header">
                    <strong>{account.account_name}</strong>
                    <span className="account-type">{account.account_type}/{account.account_subtype}</span>
                  </div>
                  <div className="account-details">
                    <div>Account: •••• {account.account_number.toString().slice(-4)}</div>
                    <div>Routing: {account.routing_number}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        
        <section className="payments-section">
          <h2>Payments</h2>
          <PaymentList adminId={adminId} />
        </section>
      </main>
    </div>
  );
}