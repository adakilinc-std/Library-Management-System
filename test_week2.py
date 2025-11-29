# test_week2.py
from patron import load_patrons, save_patrons, register_patron, authenticate_patron, list_all_patrons

patrons = load_patrons("data/patrons.json")
print(f"Loaded patron(s) count: {len(patrons)}")

new_member = {
    "name": "Ayse Demir",
    "email": "ayse@example.com",
    "library_id": "002",
    "password": "pass",
    "phone": "555-111-2222"
}
register_patron(patrons, new_member)
print("Ayse added.")

user = authenticate_patron(patrons, "002", "pass")
if user:
    print(f"Signed in: {user['name']}")
else:
    print("Sign in failed.")

save_patrons("data/patrons.json", patrons)

print(f"ALL PATRONS: {list_all_patrons(patrons)}")
