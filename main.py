from address_book import Record, AddressBook
from errors_handler import input_error


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "✅ Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "✅ Contact added"
    if phone:
        record.add_phone(phone)
    return message

@input_error
def show_phone(args: list,  book: AddressBook) -> str:
    name = args[0]
    return book.find(name)

@input_error
def change_contact(contact_for_change: list, book: AddressBook) -> str:
    name, old_phone, new_phone = contact_for_change
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "✅ Contact updated"

@input_error
def show_all(book: AddressBook) -> str:
    if not book:
        return "📒 Contact book is empty"

    printed_contatcs = ""
    for name, info in book.items():
        phones = ""
        for phone in info.phones:
            phones += str(phone)
        printed_contatcs += f"📒: {name} 📱: {phones}\n"
    return printed_contatcs

@input_error
def add_birthday(args: list, book:AddressBook) -> str:
    b_day, name, *_  = args
    book.set_birthday(b_day, name)
    return "🎉 Birthday added"

@input_error
def show_birthday(args: list, book:AddressBook) -> str:
    name = args[0]
    b_day = book.display_contact_birthday(name)
    return b_day

@input_error
def birthdays(args: list, book:AddressBook) -> str:
    upcoming_birthdays = book.get_upcoming_birthdays()
    print(upcoming_birthdays)
    for info in upcoming_birthdays:
        pass


def main():
    book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *info = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(info, book))

        elif command == "change":
            print(change_contact(info, book))

        elif command == "phone":
            print(show_phone(info, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(info, book))

        elif command == "show-birthday":
            print(show_birthday(info, book))

        elif command == "birthdays":
            print(birthdays())

        else:
            print("❌ Invalid command")


if __name__ == "__main__":
    main()
