class Book:
    def __init__(self,title,author,isbn,status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - Status: {self.status}"
    
    def to_line(self):
        return f"{self.title},{self.author},{self.isbn},{self.status}\n"
    @staticmethod
    def from_line(line):
        title, author, isbn, status = line.strip().split(',')
        return Book(title, author, isbn, status)
    
    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False
    
    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False
    
    def is_available(self):
        return self.status == "available"
    
    class Library_inventory:
        def __init__(self):
            self.books = []

        def add_book(self,book):
            self.books.append(book)

        def search_by_title(self,title):
            return [book for book in self.books if book.title.lower() == title.lower()]
        
        def search_by_author(self,author):  
            return [book for book in self.books if book.author.lower() == author.lower()]
        
        def search_by_isbn(self,isbn):
            for book in self.books:
                if book.isbn == isbn:
                    return book
            return None
        
        def display_books(self):
            for book in self.books:
                print(book)
        
        def save_inventory (inventory, filename="books.txt"):
            try:
                with open(filename , 'w') as file:
                    for book in inventory.books:
                        file.write(f"{book.title},{book.author},{book.isbn},{book.status}\n")
                print("Book saved to file")

            except Exception as e:
                print(f"An error occurred while saving the inventory: {e}")
                
    def load_inventory(filename="books.txt"):
        Library = Library()
        try:
            with open(filename, 'r') as file:
                for line in file:
                    title, author, isbn, status = line.strip().split(',')
                    book = Book(title, author, isbn, status)
                    Library.add_book(book)
            print("Inventory loaded from file")
        except FileNotFoundError:
            print("No inventory file found. Starting with an empty library.")
        except Exception as e:
            print(f"An error occurred while loading the inventory: {e}")
        return Library
    
    def main():
        library = library()

        book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
        book2 = Book("1984", "George Orwell", "9780451524935")
        book3 = Book("To Kill a Mockingbird", "Harper Lee", "9780061120084")

        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)

        print("Library Inventory:")
        library.display_books()

        print(library.issue_book("9780451524935"))

        print(library.issue_book("9780451524935"))

        print(library.return_book("9780451524935"))

        library.save_inventory(library)

        loaded_library = library.load_inventory()
        print("Loaded Library Inventory:")
        loaded_library.display_books()

        



        

        

        