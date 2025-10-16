
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import os

from backend.parser import parse_bank_sms
from backend.categorize import load_model, train_model

app = FastAPI(title="Bank SMS Expense Tracker API")

# Ensure model exists
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "category_model.joblib")
if not os.path.exists(MODEL_PATH):
    train_model()

model = load_model()

# In-memory storage (replace with DB later)
transactions = []
next_id = 1

class MessageIn(BaseModel):
    text: str

class TransactionOut(BaseModel):
    id: int
    merchant: Optional[str]
    amount: Optional[float]
    currency: Optional[str]
    category: Optional[str]
    datetime: Optional[str]

@app.post("/ingest", response_model=TransactionOut)
def ingest(msg: MessageIn):
    global next_id
    parsed = parse_bank_sms(msg.text)
    merchant = (parsed.get("merchant") or "").strip()
    category = "Uncategorized"
    try:
        if merchant:
            category = model.predict([merchant])[0]
    except Exception:
        pass

    tx = {
        "id": next_id,
        "merchant": merchant or None,
        "amount": parsed.get("amount"),
        "currency": parsed.get("currency"),
        "category": category,
        "datetime": parsed.get("datetime"),
    }
    transactions.append(tx)
    next_id += 1
    return tx

@app.get("/transactions", response_model=List[TransactionOut])
def list_transactions():
    return transactions
