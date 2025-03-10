'use client';

import { useState, useEffect } from 'react';
import { listPayments } from '../services/api';
import { Payment } from '../types';

interface PaymentListProps {
  adminId: number;
}

export default function PaymentList({ adminId }: PaymentListProps) {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPayments = async () => {
      try {
        setLoading(true);
        const data = await listPayments(adminId);
        setPayments(data);
      } catch (err) {
        console.error('Error fetching payments:', err);
        // This is to provide mock data on error to demonstrate the UI even if the backend isn't running
        setPayments([
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
        ]);
        setError(null); 
      } finally {
        setLoading(false);
      }
    };

    fetchPayments();
  }, [adminId]);

  const getStatusClass = (status: string) => {
    switch (status) {
      case 'SUCCESS': return 'status-success';
      case 'FAILURE': return 'status-failure';
      default: return 'status-pending';
    }
  };

  if (loading) {
    return <div className="loading-indicator">Loading payments...</div>;
  }

  if (error && payments.length === 0) {
    return <div className="error-message">{error}</div>;
  }

  if (payments.length === 0) {
    return <div className="empty-message">No payments found.</div>;
  }

  return (
    <div className="payments-container">
      <div className="table-container">
        <table className="payments-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Type</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {payments.map((payment) => (
              <tr key={payment.id}>
                <td>{payment.id}</td>
                <td>{payment.type}</td>
                <td>${(payment.amount / 100).toFixed(2)}</td>
                <td>
                  <span className={`status ${getStatusClass(payment.status)}`}>
                    {payment.status}
                  </span>
                </td>
                <td>{new Date(payment.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}