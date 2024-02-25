from datetime import datetime as dt, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def is_valid(self, value):
        return True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value): # Вбив би той date!
        if not self.is_valid(value):
            raise ValueError
        else:
            self._value = value

    def __str__(self) -> str:
        return str(self.value)


class Birthday(Field):
    
    def is_valid(self, value):
        try:
            dt.strptime(value, "%d.%m.%Y")
        except:
            return False
        return True
        
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError
        else:
            self.__value = dt.strptime(value, '%d.%m.%Y')

class Name(Field):
    
    def is_valid(self, value):
        return bool(value)


class Phone(Field):
    
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()


class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.birthday = None
        self.phones: list(Phone) = []

    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday}, phones: {'; '.join(str(p) for p in self.phones)}"

    def add_phone(self, phone: Phone):
        phone_obj = Phone(phone)
    
        # Перевірка на унікальність
        for p in self.phones:
            if  p.value == phone_obj.value:
                return "Phone already exist."  
        # Якщо все гаразд, додаємо телефон до списку
        self.phones.append(phone_obj)
        return phone_obj

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone: str):
        self.phones = list(filter(lambda p: p.value != phone, self.phones))

    def edit_phone(self, phone: str, new_phone: str):
        if self.find_phone(phone):
            self.remove_phone(phone)
            self.add_phone(new_phone)
        else:
            raise ValueError


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)
        
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self: dict) -> tuple:
        reminder_list = []
        reminder_string = ""

        if not self.data:
            return "Нема привітань."

        for user, record in self.data.items():
            if record.birthday == None:
                continue
            
            now = dt.today().date() # Сьогоднішня дата
            birthday = record.birthday.value.date()
            birthday = birthday.replace(year=now.year) # Теперішній рік для ДН

            if birthday < now: # Якщо пройшов встановлюємо слідующий рік
                birthday = birthday.replace(year=now.year + 1)

            until_the_birthday = birthday - now # Різниця дат

            if 0 <= until_the_birthday.days <= 7: # Умова при якій буде виводить дні на тиждень вперед
                reminder = {'name': user, 'congratulation_date': None} # Шаблон словника
                weekday = birthday.isoweekday() # День тижня

                match weekday:
                    # Якщо субота + 2 дні
                    case 6:
                        after_weekend = birthday + timedelta(days=2)
                        reminder['congratulation_date'] = after_weekend.isoformat()
                        # Неділя + 1 день
                    case 7:
                        after_weekend = birthday + timedelta(days=1)
                        reminder['congratulation_date'] = after_weekend.isoformat()
                        # Якщо будні то просто верне дату
                    case _:
                        reminder['congratulation_date'] = birthday.isoformat()
                        
                # Добавляємо нагадувалку в список
                reminder_list.append(reminder)
                reminder_string += f"name: {reminder['name']}, greet: {reminder['congratulation_date']}\n"
                
        # Повертаємо список словників та рядок з привітаннями для комфорта.
        return reminder_string, reminder_list

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
