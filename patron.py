import json
from typing import List, Dict, Any, Optional

Patron = Dict[str, Any]

def load_patrons(path:str) -> List[Patron]:
    try:
        with open(path, "r", encoding = "utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_patrons(path: str, patrons: List[Patron]) -> None:
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(patrons, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error saving patrons to {path}: {e}")

def register_patron(patrons: List[Patron], patron_data: Patron) -> Optional[Patron]:
    new_id = patron_data.get("library_id")
    if not new_id:
        print("Library ID is required to register a patron.")
        return None
    
    for patron in patrons:
        if patron.get("library_id") == new_id:
            print(f"Patron with library ID {new_id} already exists.")
            return None
    
    patron_data.setdefault("fines_owed",0.0)
    patron_data.setdefault("current_loans",[])
    patron_data.setdefault("history",[])
    patron_data.setdefault("max_limit", 5)

    patrons.append(patron_data)
    return patron_data

def authenticate_patron(patrons: List[Patron], library_id: str, password: str) -> Optional[Patron]:
    for patron in patrons:
        if patron.get("library_id") == library_id and patron.get("password") == password:
            return patron
    return None

def update_patron_contact(patrons: List[Patron], library_id: str, contact_updates: Dict[str, str]) -> Optional[Patron]:
    for patron in patrons:
        if patron.get("library_id") == library_id:
            if "email" in contact_updates:
                patron["email"] = contact_updates["email"]
            if "phone" in contact_updates:
                patron["phone"] = contact_updates["phone"]
            if "address" in contact_updates:
                patron["address"] = contact_updates["address"]
            return patron
    return None

def get_patron_by_id(patrons: List[Patron], library_id: str) -> Optional[Patron]:
    for patron in patrons:
        if patron.get("library_id") == library_id:
            return patron
    return None

def list_all_patrons(patrons: List[Patron]) -> List[Patron]:
    return patrons


