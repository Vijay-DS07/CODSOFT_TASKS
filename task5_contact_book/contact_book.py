"""Contact Book (CodSoft Python Internship - Task 5).

Store, view, search, update, and delete contacts.
Contacts are saved to contacts.json so they persist between runs.
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.json")


def load_contacts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_contacts(contacts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2)


def print_contact(c):
    print(f"  Name   : {c['name']}")
    print(f"  Phone  : {c['phone']}")
    print(f"  Email  : {c['email'] or '-'}")
    print(f"  Address: {c['address'] or '-'}")
    print("  " + "-" * 30)


def ask(prompt, required=False, current=None):
    """Ask for input. If `current` is given, blank keeps the current value."""
    if current is not None:
        value = input(f"{prompt} [{current}]: ").strip()
        return value if value else current
    value = input(f"{prompt}: ").strip()
    while required and not value:
        print("This field is required.")
        value = input(f"{prompt}: ").strip()
    return value


def find_by_phone(contacts, phone):
    return next((c for c in contacts if c["phone"] == phone), None)


def add_contact(contacts):
    name = ask("Name", required=True)
    phone = ask("Phone", required=True)
    if find_by_phone(contacts, phone):
        print("A contact with this phone number already exists.")
        return
    email = ask("Email")
    address = ask("Address")
    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    contacts.sort(key=lambda c: c["name"].lower())
    save_contacts(contacts)
    print("Contact added.")


def view_contacts(contacts):
    if not contacts:
        print("\nNo contacts saved.")
        return
    print()
    for c in contacts:
        print(f"  {c['name']:<25} {c['phone']}")
    print()


def search_contacts(contacts):
    query = input("Search by name or phone: ").strip().lower()
    if not query:
        print("Nothing to search for.")
        return
    matches = [
        c for c in contacts
        if query in c["name"].lower() or query in c["phone"]
    ]
    if not matches:
        print("No matching contacts.")
        return
    print()
    for c in matches:
        print_contact(c)


def pick_contact(contacts):
    """Find a contact by exact phone number. Returns the contact or None."""
    phone = input("Enter the contact's phone number: ").strip()
    contact = find_by_phone(contacts, phone)
    if contact is None:
        print("No contact found with that phone number.")
    return contact


def update_contact(contacts):
    contact = pick_contact(contacts)
    if contact is None:
        return
    print("Press Enter to keep the current value.")
    contact["name"] = ask("Name", current=contact["name"])
    contact["email"] = ask("Email", current=contact["email"])
    contact["address"] = ask("Address", current=contact["address"])
    new_phone = ask("Phone", current=contact["phone"])
    if new_phone != contact["phone"] and find_by_phone(contacts, new_phone):
        print("Another contact already uses that phone number. Changes to phone not saved.")
    else:
        contact["phone"] = new_phone
    contacts.sort(key=lambda c: c["name"].lower())
    save_contacts(contacts)
    print("Contact updated.")


def delete_contact(contacts):
    contact = pick_contact(contacts)
    if contact is None:
        return
    confirm = input(f"Delete {contact['name']}? (y/n): ").strip().lower()
    if confirm == "y":
        contacts.remove(contact)
        save_contacts(contacts)
        print("Contact deleted.")
    else:
        print("Deletion cancelled.")


def main():
    contacts = load_contacts()
    menu = """
========== CONTACT BOOK ==========
1. Add contact
2. View all contacts
3. Search contact
4. Update contact
5. Delete contact
6. Exit
==================================="""
    actions = {
        "1": add_contact,
        "2": view_contacts,
        "3": search_contacts,
        "4": update_contact,
        "5": delete_contact,
    }
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        if choice in actions:
            actions[choice](contacts)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
