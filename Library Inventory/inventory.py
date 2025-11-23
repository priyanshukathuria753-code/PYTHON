import logging
from pathlib import Path
from book import Book

logging.basicConfig(filename="library.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class LibraryInventory:
    def _init__ (self,file_path="catolog.txt"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_inventory()

    def load_data(self):
        try:
            if not self.file_path.exists():
                self.file_path.write_text("")

            with open(self.file_path, 'r') as file:
                for line in file:
                    if line.strip():
                        self.books.append(Book.from_line(line))

        except Exception as e:
            logging.error(f"Error loading file: {e}")
    
    def save_data(self):
        try:
            with open(self.file_path, 'w') as file:
                for book in self.books:
                    file.write(book.to_line())
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def add_book(self,title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_data()
        logging.info(f"Added book: {new_book}")

    def search_by_title(self,title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_author(self,isbn): 
        return next((b for b in self.books if b.isbn == isbn), None)
    
    def display_all(self):
        return self.books
    
    