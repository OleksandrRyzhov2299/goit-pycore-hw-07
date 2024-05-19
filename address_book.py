from collections import UserDict
from datetime import datetime, timedelta


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
            self.value = parsed_date
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
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def set_birthday(self, name, date):
        contact = self.find(name)
        if contact:
            contact.add_birthday(date)

    def display_contact_birthday(self, name):
        contact = self.find(name)
        if contact and contact.birthday:
            formated_b_day = contact.birthday.value.strftime("%d.%m.%Y")
            return formated_b_day
        else:
            raise AttributeError("🔴 Contact does not have a birthday")

    def get_upcoming_birthdays(self):
        CURRENT_DATE = datetime.today().date()
        upcoming_birthdays = []

        for info in self.data.values():
            name = info.name.value
            birthday = info.birthday.value.date()
            birthday_this_year = birthday.replace(year=CURRENT_DATE.year)

            if birthday_this_year < CURRENT_DATE:
                birthday_this_year = birthday.replace(year=CURRENT_DATE.year + 1)

            delta_days = (birthday_this_year - CURRENT_DATE).days

            if delta_days < 7:
                formatted_date = birthday_this_year.strftime("%d.%m.%Y")

                if birthday_this_year.weekday() >= 5:
                    days_until_monday = (7 - birthday_this_year.weekday()) % 7
                    next_monday = birthday_this_year + timedelta(days=days_until_monday)
                    formatted_date = next_monday.strftime("%d.%m.%Y")

                upcoming_birthdays.append(
                    {
                        "name": name,
                        "congratulation_date": formatted_date,
                    }
                )

        return upcoming_birthdays
