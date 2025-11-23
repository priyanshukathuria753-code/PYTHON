from inventory import LibraryInventory

Inventory = LibraryInventory ()

def menu():
    print("\n==== Library Inventory Manager  ====")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")

while True:
    menu()
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input.")
        continue
    
    if choice == 1:
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter book ISBN: ")
        Inventory.add_book(title, author, isbn)
        print("Book added successfully.")

    elif choice == 2:
        isbn = input("Enter book ISBN to issue: ")
        book = Inventory.search_by_author(isbn)
        if book and book.issue():
            Inventory.save_data()
            print("Book issued successfully.")
        else:
            print("Book not available for issue.")

    elif choice == 3:
        isbn = input("Enter book ISBN to return: ")
        book = Inventory.search_by_author(isbn)
        if book and book.return_book():
            Inventory.save_data()
            print("Book returned successfully.")
        else:
            print("Book not found or not issued.")

    elif choice == 4:
        for b in Inventory.display_all():
            print(b)

    elif choice == 5:
        keyword= input("Enter title keyword to search: ")
        results = Inventory.search_by_title(keyword)
        if results:
            for b in results:
                print(b)
        else:
            print("No books found with that title.")

    elif choice == 6:
        print("Goodbye!,have a nice day.")
        break
    else:
        print("Invalid choice")
        