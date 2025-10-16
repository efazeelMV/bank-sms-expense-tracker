
import re
from datetime import datetime
from decimal import Decimal

def parse_bank_sms(text: str):
    # Parse bank SMS-like notifications into structured fields.
    result = {
        "raw": text,
        "card_tail": None,
        "date": None,
        "time": None,
        "datetime": None,
        "currency": None,
        "amount": None,
        "merchant": None,
        "reference_no": None,
        "approval_code": None,
    }

    # Card/account tail
    m = re.search(r'(?:from|card|acct|a/c|a/c no\.?)\s*([0-9]{2,4})', text, re.I)
    if m:
        result["card_tail"] = m.group(1)

    # Date: dd/mm/yy or dd/mm/yyyy or yyyy-mm-dd
    date_match = re.search(r'(\b[0-3]?\d[\/\-][0-1]?\d[\/\-][0-9]{2,4}\b)', text)
    if date_match:
        date_str = date_match.group(1)
        for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(date_str, fmt)
                result["date"] = date_str
                result["date_obj"] = dt.date()
                break
            except Exception:
                pass

    # Time: hh:mm[:ss]
    time_match = re.search(r'(\b[0-2]?\d:[0-5]\d(?::[0-5]\d)?\b)', text)
    if time_match:
        result["time"] = time_match.group(1)
        if result.get("date_obj"):
            try:
                fmt = "%H:%M:%S" if result["time"].count(":") == 2 else "%H:%M"
                t = datetime.strptime(result["time"], fmt).time()
                result["datetime"] = datetime.combine(result["date_obj"], t).isoformat()
            except Exception:
                pass

    # Amount & currency
    amount_match = re.search(r'([A-Z]{2,4})\s*([0-9,]+(?:\.[0-9]{1,2})?)|([0-9,]+(?:\.[0-9]{1,2})?)\s*(MVR|USD|INR|EUR|SGD)?', text)
    if amount_match:
        currency = amount_match.group(1) or amount_match.group(4)
        amount_str = amount_match.group(2) or amount_match.group(3)
        if currency:
            result["currency"] = currency.strip()
        if amount_str:
            try:
                result["amount"] = float(Decimal(amount_str.replace(",", "")))
            except Exception:
                pass

    # Merchant
    m2 = re.search(r'\b(?:at|to|in|for)\s+([A-Z0-9 &\'\-.\/]{2,60})', text, re.I)
    if m2:
        merchant = re.split(r'\b(?:was|processed|ref|reference|txn)\b', m2.group(1), flags=re.I)[0].strip(' ,.')
        result["merchant"] = merchant.upper()

    # Reference No
    ref = re.search(r'Reference\s*No[:\s]*([0-9A-Z\-]+)', text, re.I)
    if ref:
        result["reference_no"] = ref.group(1)

    # Approval Code
    app = re.search(r'Approval\s*Code[:\s]*([0-9A-Z\-]+)', text, re.I)
    if app:
        result["approval_code"] = app.group(1)

    return result
