#!/bin/bash
python3 -m uvicorn auth_service.main:app --port 8000
