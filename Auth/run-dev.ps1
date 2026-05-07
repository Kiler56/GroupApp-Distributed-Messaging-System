# Create/Activate environment
if (!(Test-Path "venv")) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run service
python -m uvicorn auth_service.main:app --port 8000 --reload
