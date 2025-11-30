# test_week3.py
from catalog import load_books, save_books
from patron import load_patrons, save_patrons
from circulation import checkout_book, return_book, load_loans, save_loans, list_all_loans, overdue_loans

# 1. Load Data
books = load_books("data/books.json")
patrons = load_patrons("data/patrons.json")
loans = load_loans("data/loans.json")

print("--- INITIAL STATE ---")
print(f"Book Stock (Copies): {books[0].get('copies_available', 0)}")
print(f"Patron Loan Count: {len(patrons[0].get('current_loans', []))}")    

# 2. Checkout Process
print("\n--- CHECKOUT PROCESS ---")
isbn_to_borrow = "9780000000001"
user_id = "001" 

result = checkout_book(books, patrons, loans, isbn_to_borrow, user_id)
print(f"Result: {result['message']}")

if result['success']:
    loan_id = result['loan']['loan_id']
    print(f"Generated Loan ID: {loan_id}")
    print(f"New Book Stock: {books[0]['copies_available']}") 
    
    # 3. Return Process
    print("\n--- RETURN PROCESS ---")
    # Returning immediately
    return_result = return_book(books, patrons, loans, loan_id)
    print(f"Return Result: {return_result['message']}")
    # Should be 1 again
    print(f"Stock After Return: {books[0]['copies_available']}") 

# 4. Save Results
save_loans("data/loans.json", loans)
save_books("data/books.json", books)
save_patrons("data/patrons.json", patrons)

print("\n--- ALL LOANS ---")
all_loans_list = list_all_loans(loans)
for loan in all_loans_list:
    print(loan)

print("\n--- OVERDUE LOANS ---")
overdues = overdue_loans(loans)
if not overdues:
    print("No overdue books found.")
else:
    for overdue in overdues:
        print(overdue)