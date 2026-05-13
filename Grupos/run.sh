#!/bin/bash
export PYTHONPATH="..:$PYTHONPATH"
python3 -m uvicorn main:app --port 8002
