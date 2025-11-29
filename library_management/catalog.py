import json
from typing import List, Dict, Any, Optional

Book = Dict[str, object] # Define a type alias for reading clarity

def load_books(path: str) -> List[Book]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(path: str, books: List[Book]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def add_book(books: List[Book], book_data: Book) -> Any:
    new_isbn = book_data.get("isbn")
    if not new_isbn:
        return None

    for b in books:
        if b.get("isbn") == new_isbn:
            return None

    copies_owned = book_data.get("copies_owned", 1)
    book_data.setdefault("copies_owned", copies_owned)
    book_data.setdefault("copies_available", copies_owned) # For new books, available copies equal owned copies
    book_data.setdefault("active", True) # Soft delete flag

    books.append(book_data)
    return book_data

def update_book(books: List[Book], isbn: str, updates: Dict[str, object]) -> Any:
    for b in books:
        if b.get("isbn") == isbn:
            b.update(updates)
            return b
    return None

def search_books(books: List[Book], keyword: str) -> List[Book]:
    keyword_lower = keyword.lower()
    result = []

    for b in books:
        if not b.get("active", True):
            continue

        title = str(b.get("title", "")).lower()
        genre = str(b.get("genre", "")).lower()
        isbn = str(b.get("isbn", "")).lower()
        authors = b.get("authors", [])

        if isinstance(authors, list):
            authors_str = " ".join(str(a) for a in authors).lower()
        else:
            authors_str = str(authors).lower()

        if (keyword_lower in title
            or keyword_lower in genre
            or keyword_lower in isbn
            or keyword_lower in authors_str):
            result.append(b)

    return result

def filter_books(books: List[Book], *, genre: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
    result = []

    for b in books:
        if not b.get("active", True):
            continue

        if genre is not None:
            if str(b.get("genre", "")).lower() != genre.lower():
                continue

        if year is not None:
            try:
                book_year = int(b.get("year"))
            except (TypeError, ValueError):
                continue

            if book_year != year:
                continue

        result.append(b)

    return result

