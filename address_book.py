from collections import UserDict
from datetime import datetime, timedelta
from errors_handler import input_error

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        self.name = Field(name)


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 and not value.isdigit():
            raise ValueError()
        self.value = value


class Birthday(Field):
    def __init__(self, value, format="%d.%m.%Y"):
        try:
            parsed_date = datetime.strptime(value, format)
            self.value = Field(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birth_date):
        if self.birthday is None:
            self.birthday = Birthday(birth_date)

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                search_index = self.phones.index(phone)
                del self.phones[search_index]
                return True
        return False

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                search_index = self.phones.index(phone)
                self.phones[search_index] = Phone(new_phone_number)
                break

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record

    def find(self, name):
        for record_name, record in self.data.items():
            if name == record_name.name.value:
                return record

    def delete(self, name):
        for record_name, record in self.data.items():
            if name == record_name.name.value:
                del self.data[record_name]
                return True
        return False
    
    def set_birthday(self, name, date):
        contact = self.find(name)
        contact.add_birthday(date)

    def display_contact_birthday(self, name):
        contact = self.find(name)
        if contact.birthday:
            return contact.birthday.value
        else:
            raise AttributeError("🔴 Contact does not have a birthday")

    def get_upcoming_birthdays(self):
        current_date = datetime.today().date()
        upcoming_birthdays = []

        for info in self.data.values():
            name = info.name.value()
            birthday = datetime.strptime(str(info.birthday), "%d.%m.%Y").date()
            birthday_this_year = birthday.replace(year=current_date.year)

            if birthday_this_year < current_date:
                birthday_this_year = birthday.replace(year=current_date.year + 1)

            delta_days = (birthday_this_year - current_date).days

            if delta_days < 7:
                formated_date = datetime.strftime(birthday_this_year, "%d.%m.%Y")

                if birthday_this_year.weekday() >= 5:
                    days_until_monday = (7 - birthday_this_year.weekday()) % 7
                    next_monday = birthday_this_year + timedelta(days=days_until_monday)
                    formated_date = datetime.strftime(next_monday, "%d.%m.%Y")

                upcoming_birthdays.append(
                    {
                        "name": name,
                        "congratulation_date": formated_date,
                    }
                )

        return upcoming_birthdays

