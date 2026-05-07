#!/bin/bash
# Create/Activate environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run service
python3 -m uvicorn app.main:app --port 8003 --reload
