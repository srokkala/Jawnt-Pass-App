# Jawnt Technical Assessment
<img width="1510" alt="Screenshot 2025-03-10 at 2 48 46 AM" src="https://github.com/user-attachments/assets/49ac2502-c0f1-48dd-938f-e10bffe8b32e" />

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


<img width="1512" alt="Screenshot 2025-03-10 at 2 54 42 AM" src="https://github.com/user-attachments/assets/88c30323-6edc-4773-bfb1-20c14294c9f0" />

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

