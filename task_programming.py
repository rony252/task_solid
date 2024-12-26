# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 17:20:38 2024

@author: CompuStore
"""

from abc import ABC, abstractmethod

# S: Single Responsibility Principle
# Each class has a single responsibility.

class Book:
    """Represents a book."""
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year


class Member:
    """Represents a library member."""
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id


# O: Open/Closed Principle
# Classes are open for extension but closed for modification.

class NotificationService(ABC):
    """Abstract class for sending notifications."""
    @abstractmethod
    def notify(self, member, message):
        pass


class EmailNotification(NotificationService):
    """Sends notifications via email."""
    def notify(self, member, message):
        print(f"Email to {member.name}: {message}")


class SMSNotification(NotificationService):
    """Sends notifications via SMS."""
    def notify(self, member, message):
        print(f"SMS to {member.name}: {message}")


# L: Liskov Substitution Principle
# Subclasses can replace their parent classes without breaking functionality.

class LibraryInventory:
    """Manages the library's inventory of books."""
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def list_books(self):
        return [f"{book.title} by {book.author}" for book in self.books]


# I: Interface Segregation Principle
# Avoid forcing classes to implement unused methods.

class LoanService(ABC):
    """Abstract class for loan services."""
    @abstractmethod
    def loan_book(self, member, book):
        pass

    @abstractmethod
    def return_book(self, member, book):
        pass


class BasicLoanService(LoanService):
    """Manages book loans."""
    def __init__(self):
        self.loans = {}

    def loan_book(self, member, book):
        if member not in self.loans:
            self.loans[member] = []
        self.loans[member].append(book)
        print(f"{book.title} loaned to {member.name}.")

    def return_book(self, member, book):
        if member in self.loans and book in self.loans[member]:
            self.loans[member].remove(book)
            print(f"{book.title} returned by {member.name}.")
        else:
            print(f"{member.name} does not have {book.title}.")

# D: Dependency Inversion Principle
# High-level modules depend on abstractions, not concrete implementations.

class LibraryService:
    """High-level service that depends on abstractions."""
    def __init__(self, inventory: LibraryInventory, loan_service: LoanService, notifier: NotificationService):
        self.inventory = inventory
        self.loan_service = loan_service
        self.notifier = notifier

    def add_book_to_inventory(self, book):
        self.inventory.add_book(book)
        print(f"{book.title} added to the library.")

    def loan_book_to_member(self, member, book):
        if book in self.inventory.books:
            self.loan_service.loan_book(member, book)
            self.inventory.remove_book(book)
            self.notifier.notify(member, f"You have loaned '{book.title}'.")
        else:
            print(f"'{book.title}' is not available in the inventory.")

    def return_book_from_member(self, member, book):
        self.loan_service.return_book(member, book)
        self.inventory.add_book(book)
        self.notifier.notify(member, f"Thank you for returning '{book.title}'.")
# Creating Objects
# Inventory for books
inventory = LibraryInventory()

# Notification service
notifier = EmailNotification()

# Loan service
loan_service = BasicLoanService()

# Library service
library_service = LibraryService(inventory, loan_service, notifier)

# Books
book1 = Book("Clean Code", "Robert C. Martin", 2008)
book2 = Book("The Pragmatic Programmer", "Andrew Hunt", 1999)
book3 = Book("Design Patterns", "Gang of Four", 1994)

# Members
member1 = Member("Alice", "M001")
member2 = Member("Bob", "M002")

# --- Adding Books to Inventory ---
library_service.add_book_to_inventory(book1)
library_service.add_book_to_inventory(book2)
library_service.add_book_to_inventory(book3)

# --- Loaning Books ---
library_service.loan_book_to_member(member1, book1)
library_service.loan_book_to_member(member2, book2)

# --- Returning Books ---
library_service.return_book_from_member(member1, book1)
library_service.return_book_from_member(member2, book2)

# --- Listing Available Books ---
print("Books currently in inventory:")
for book in inventory.list_books():
    print(book)
