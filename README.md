# ScalePilot AI

Predictive Auto-Scaling of Cloud Applications Using Machine Learning
(Flask + scikit-learn + SQLite + Chart.js)

## Folder structure
```
scalepilot-ai/
├── app.py              <- main backend (Flask + ML model + SQLite)
├── templates/
│   └── index.html      <- dashboard page
├── requirements.txt    <- Python libraries
├── test_app.py         <- quick self-test
├── Dockerfile          <- optional (Docker)
├── .gitignore
└── README.md
```

## Run on Windows (PowerShell / CMD)
```
cd scalepilot-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python test_app.py
python app.py
```
Browser: http://127.0.0.1:5000

## Optional: Docker
```
docker build -t scalepilot-ai .
docker run -p 5000:5000 scalepilot-ai
```
