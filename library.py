import lms_core

def main_menu():
    lms_core.setup_db()  # Make sure DB & tables exist

    while True:
        print("\n===== Library Management System =====")
        print("1. Add Book")
        print("2. View All Books (Sorted by Title)")
        print("3. Search Book by Title")
        print("4. Delete Book by ID")
        print("5. Add Member")
        print("6. View Members")
        print("7. Issue Book")
        print("8. Return Book")
        print("9. View Issued Books")
        print("10. View Issue & Return History")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Title: ")
            author = input("Author: ")
            publisher = input("Publisher: ")
            genre = input("Genre: ")
            quantity = int(input("Quantity: "))
            lms_core.add_book(title, author, publisher, genre, quantity)
            print("Book added!")

        elif choice == '2':
            books = lms_core.get_all_books()
            sorted_books = lms_core.bubble_sort_books(books)  # Bubble Sort
            print("\n===== All Books (Sorted) =====")
            for book in sorted_books:
                print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Qty: {book[5]}")

        elif choice == '3':
            title = input("Enter title to search: ")
            results = lms_core.search_books_by_title(title)
            if results:
                print("\n===== Search Results =====")
                for book in results:
                    print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Qty: {book[5]}")
            else:
                print("No matching books found.")

        elif choice == '4':
            book_id = int(input("Enter Book ID to delete: "))
            lms_core.delete_book(book_id)
            print("Book deleted (if ID existed).")

        elif choice == '5':
            name = input("Member Name: ")
            contact = input("Contact: ")
            lms_core.add_member(name, contact)
            print("Member added!")

        elif choice == '6':
            members = lms_core.get_all_members()
            print("\n===== Members =====")
            for m in members:
                print(f"ID: {m[0]} | Name: {m[1]} | Contact: {m[2]}")

        elif choice == '7':
            # Show books and members to pick IDs easily
            print("\nAvailable Books:")
            books = lms_core.get_all_books()
            sorted_books = lms_core.bubble_sort_books(books)
            for book in sorted_books:
                print(f"ID: {book[0]} | Title: {book[1]} | Qty: {book[5]}")

            print("\nRegistered Members:")
            members = lms_core.get_all_members()
            for m in members:
                print(f"ID: {m[0]} | Name: {m[1]}")

            book_id = int(input("Enter Book ID to issue: "))
            member_id = int(input("Enter Member ID: "))
            if lms_core.issue_book(book_id, member_id):
                print("Book issued!")
            else:
                print("Book not available or invalid ID.")

        elif choice == '8':
            issued = lms_core.get_issued_books()
            if issued:
                print("\n===== Issued Books =====")
                for i in issued:
                    if i[4] is None:
                        print(f"Issue ID: {i[0]} | Title: {i[1]} | Member: {i[2]} | Issued: {i[3]}")
                issue_id = int(input("Enter Issue ID to return: "))
                if lms_core.return_book(issue_id):
                    print("Book returned!")
                else:
                    print("Invalid Issue ID.")
            else:
                print("No issued books found.")

        elif choice == '9':
            issued = lms_core.get_issued_books()
            if issued:
                print("\n===== Currently Issued Books =====")
                for i in issued:
                    if i[4] is None:
                        print(f"Issue ID: {i[0]} | Title: {i[1]} | Member: {i[2]} | Issued: {i[3]}")
            else:
                print("No books are currently issued.")

        elif choice == '10':
            history = lms_core.get_issued_books()
            if history:
                print("\n===== Full Issue & Return History =====")
                for h in history:
                    print(f"Issue ID: {h[0]} | Title: {h[1]} | Member: {h[2]} | Issued: {h[3]} | Returned: {h[4]}")
            else:
                print("No issue history found.")

        elif choice == '11':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()