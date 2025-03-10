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
pip install fastapi uvicorn pydantic
```

3. Run the application:
```bash
uvicorn main:app --reload
```

4. API will be available at http://localhost:8000
   - API documentation available at http://localhost:8000/docs

