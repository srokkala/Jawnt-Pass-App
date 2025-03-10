# Jawnt Backend Setup Guide

This is the backend implementation for the Jawnt challenge.

## Getting Started

1. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

4. API will be available at http://localhost:8000
   - API documentation available at http://localhost:8000/docs

## Running Tests

### Using unittest

Run all tests in the tests directory:
```bash
python -m unittest discover tests
```

Run a specific test file:
```bash
python -m unittest tests.test_payments
```

Run a specific test method:
```bash
python -m unittest tests.test_payments.TestPayments.test_create_payment
```
