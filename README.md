
# 💳 Bank SMS Expense Tracker (AI)

Turn pasted **bank SMS debit alerts** into categorized expenses automatically.

## Features
- Extracts amount, merchant, date/time, ref/approval codes from bank SMS text.
- Categorizes spending via AI (TF‑IDF + Logistic Regression).
- REST API built with FastAPI.
- Tiny React Native screen to paste a message and view result.

## Folder structure
```
bank-sms-expense-tracker/
├── backend/
│   ├── app.py
│   ├── parser.py
│   ├── categorize.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── category_model.joblib   # auto-created on first run
│   ├── data/
│   │   └── sample_training_data.csv
│   ├── __init__.py
│   └── requirements.txt
├── frontend/
│   └── PasteTransaction.js
└── .gitignore
```

## Quick start (Backend)
```bash
cd backend
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows (Powershell)
# .\venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Train model automatically (first run) and start API
uvicorn backend.app:app --reload
```

The API is available at `http://localhost:8000` and docs at `http://localhost:8000/docs`.

### Try ingest
```bash
curl -X POST http://localhost:8000/ingest   -H "Content-Type: application/json"   -d '{"text": "Transaction from 0634 on 16/10/25 at 23:37:41 for MVR58.74 at SEMILI was processed. Reference No:101690513586, Approval Code:889680."}'
```

### React Native (example)
Use `frontend/PasteTransaction.js` in your RN app and point it to your backend URL.

## Next steps
- Add a database (SQLite/Postgres) for persistence.
- Add merchant/category editing and fuzzy-merge.
- Android SMS / IMAP email connectors (optional).
- CSV export + monthly category summaries.
