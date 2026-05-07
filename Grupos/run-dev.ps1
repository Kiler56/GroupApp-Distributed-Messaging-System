# Create/Activate environment
if (!(Test-Path "venv")) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run service
$env:PYTHONPATH = ".;$env:PYTHONPATH"
python -m uvicorn Grupos.main:app --port 8002 --reload
