# Jawnt Technical Assessment

## Overview

This project implements a banking system with the following core features:

- External bank account connection via Plaid
- Internal bank account management
- ACH payment processing
- Real-time payment status tracking

## Project Structure

```
├── frontend/          
   ├── src/          
      ├── app/      # Pages and layouts
        ├── components/ # Reusable components
        ├── dashboard/    # Dashboard page
        ├── services/      # API wiring
        └── types/    # TypeScript definitions

├── backend/          
      ├── api/     # API endpoints
      ├── domain/  # Models and Database setup
      ├── lib/  # Mock payment library Responses
      ├── message_queue/ # Queue implementation
      └── tests/    # Tests
```

## API Documentation

## Tech Stack

### Frontend

- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- Plaid Link SDK
- Axios for API calls

### Backend

- FastAPI
- Python with type hints
- In-memory database
- Message queue system
- Plaid API integration

## Documentation

- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)
- [Development Tickets](./TICKETS.md)

