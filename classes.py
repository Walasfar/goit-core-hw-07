from datetime import datetime as dt, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):

    def __init__(self, value):
        super().__init__(value)
        
        if not self.validate_number():
            raise ValueError("Неправельний номер телефону. Номер має складатися з 10 цифр.")
    
    def validate_number(self):
        return len(self.value) == 10 and self.value.isdigit()


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            # Провалідуємо дату одразу, методом .strptime
            self.date = dt.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.birthday = None
        self.phones: list(Phone) = []

    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: Phone):
        phone_obj = Phone(phone)
    
        # Перевірка на унікальність
        for p in self.phones:
            if  p.value == phone_obj.value:
                return "Phone already exist."
            
        # Якщо все гаразд, додаємо телефон до списку
        self.phones.append(phone_obj)
        return "Phone added successfully."

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def delete_phone(self, phone: str):
        self.phones = list(filter(lambda p: p.value != phone, self.phones))

    def edit_phone(self, phone: str, new_phone: str):
        new_phone_obj = Phone(new_phone)
        for p in self.phones:
            if p.value == phone:
                p.value = new_phone_obj.value

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return f"{self.name.value}'s phone finded: {p.value}"
            else:
                return 'Number not found.'

    def show_phones(self):
        result = ""
        for phone in self.phones:
            result += f"{phone}\n"
        return result


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, name: str):
        try:
            return self.data[name]
        except KeyError:
            return f"Record '{name}' does not exist."
        
    def delete_record(self, name: str):
        del self.data[name]

    def show_contacts(self):
        if not self.data:
            return "Book is empty."
        result = ""
        for name, record in self.data.items():
            result += f"{record}\n"
        return result

    def get_upcoming_birthdays(self):
    
        reminder_list = ""
        
        for user, record in self.data.items():
            
            now = dt.today().date() # Сьогоднішня дата
            birthday = record.birthday.date.date()
            birthday = birthday.replace(year=now.year) # Теперішній рік для ДН

            if birthday < now: # Якщо пройшов встановлюємо слідующий рік
                birthday = birthday.replace(year=now.year + 1)

            until_the_birthday = birthday - now # Різниця дат

            if 0 <= until_the_birthday.days <= 7: # Умова при якій буде виводить дні на тиждень вперед
            
                reminder = {'name': user, 'congratulation_date': None} # Шаблон словника
                weekday = birthday.isoweekday() # День тижня
                
                match weekday:
                
                    case 6: # Якщо субота + 2 дні
                        after_weekend = birthday + timedelta(days=2)
                        reminder['congratulation_date'] = after_weekend.isoformat()
                            
                    case 7: # Неділя + 1 день
                        after_weekend = birthday + timedelta(days=1)
                        reminder['congratulation_date'] = after_weekend.isoformat()

                    case _: # Якщо будні то просто верне дату
                        reminder['congratulation_date'] = birthday.isoformat()
                        
                reminder_list += f"name: {reminder['name']}, greet: {reminder['congratulation_date']}\n" # Добавляємо нагадувалку в список

        return reminder_list # Вертаємо список
