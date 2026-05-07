#!/bin/bash
# Create/Activate environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run service
export PYTHONPATH=".:$PYTHONPATH"
python3 -m uvicorn Grupos.main:app --port 8002 --reload
