import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

Loan = Dict[str, Any]
Book = Dict[str, Any]
Patron = Dict[str, Any]

DAILY_FINE_RATE = 5.0

def load_loans(path:str) -> List[Loan]:
    try:
        with open(path, "r", encoding = "utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_loans(path: str, loans: List[Loan]) -> None:
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(loans, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error saving loans to {path}: {e}")

def checkout_book(books: List[Book], patrons: List[Patron], loans: List[Loan], isbn: str, library_id: str, loan_period_days: int = 14) -> Dict[str, Any]:
    #Find the book and check availability
    book = next((b for b in books if b.get("isbn") == isbn), None)
    if not book:
        return {"success": False, "message": "Book not found."}
    if book.get("available_copies", 0) < 1:
        return {"success": False, "message": "No available copies."}
    
    #Find the patron
    patron = next((p for p in patrons if p.get("library_id") == library_id), None)
    if not patron:
        return {"success": False, "message": "Patron not found."}
    
    #Check patron's loan limit
    current_loans_count = len(patron.get("current_loans", []))
    max_limit = patron.get("max_limit", 5)

    if current_loans_count >= max_limit:
        return {"success": False, "message": f"Patron has reached maximum loan limit ({max_limit} books)."}
    
    #Create the loan record
    today = datetime.now().date()
    due_date = today + timedelta(days=loan_period_days)

    loan_id = f"{library_id}-{isbn}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    new_loan = {
        "loan_id": loan_id,
        "isbn": isbn,
        "library_id": library_id,
        "start_date": str(today),
        "due_date": str(due_date),
        "return_date": None,
        "status": "active"
    }

    #Update book availability
    loans.append(new_loan)
    book["available_copies"] -= 1
    patron.setdefault("current_loans", []).append(loan_id)

    return {"success": True, "message": "Book checked out successfully.", "loan": new_loan}

def return_book(books:List[Book], patrons: List[Patron], loans: List[Loan], loan_id:str) -> Dict[str, Any]:
    #Find the loan
    loan = next((l for l in loans if l.get("loan_id") == loan_id), None)
    if not loan or loan["status"] != "active":
        return {"success": False, "message": "Active loan not found."}
    
    #Find the book and patron
    isbn = loan["isbn"]
    library_id = loan["library_id"]

    book = next((b for b in books if b.get("isbn") == isbn), None)
    patron = next((p for p in patrons if p.get("library_id") == library_id), None)

    if not book or not patron:
        return {"success": False, "message": "Book or Patron not found."}
    
    #Calculate fines if overdue
    today = datetime.now().date()
    due_date = datetime.strptime(loan["due_date"], "%Y-%m-%d").date()
    fine_amount = 0.0

    if today > due_date:
        overdue_days = (today - due_date).days
        fine_amount = overdue_days * DAILY_FINE_RATE
        
    #Update loan record
    loan["return_date"] = str(today)
    loan["status"] = "returned"

    book["available_copies"] += 1

    if loan_id in patron.get("current_loans", []):
        patron["current_loans"].remove(loan_id)

    patron.setdefault("history", []).append(loan_id)

    #Update patron fines
    if fine_amount > 0:
        current_fines = patron.get("fines_owed", 0.0)
        patron["fines_owed"] = current_fines + fine_amount

    return {"success": True, "message": "Book returned successfully.", "fine_amount": fine_amount}

def list_patron_loans(loans: List[Loan], library_id: str) -> List[Loan]:
    patron_loans = [loan for loan in loans if loan.get("library_id") == library_id]
    return patron_loans

def overdue_loans(loans: List[Loan]) -> List[Loan]:
    today = datetime.now().date()
    overdue = []
    for loan in loans:
        if loan["status"] == "active":
            due_date = datetime.strptime(loan["due_date"], "%Y-%m-%d").date()
            if today > due_date:
                overdue.append(loan)
    return overdue

def list_all_loans(loans: List[Loan]) -> List[Loan]:
    return loans

