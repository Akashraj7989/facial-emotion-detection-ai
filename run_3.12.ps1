# PowerShell script to create venv with Python 3.12, install deps, and run app
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
python app.py
