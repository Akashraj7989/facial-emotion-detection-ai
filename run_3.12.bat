@echo off
REM Activate Python 3.12 venv (creates if missing), install requirements, and run app.py
py -3.12 -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
python app.py
