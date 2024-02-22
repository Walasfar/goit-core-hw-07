from classes import AddressBook, Record

# Обробник помилок 
def input_error(func):
    def inner(*args, **kwargs):      
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except KeyError as e:
            return f"User - {e} not found."
        except IndexError as e:
            return f"Please enter the correct number of arguments. Error: {e}"
        # Для інших
        except Exception as e:
            return f"An unexpected error occured: Error: {e}"
        
    return inner


@input_error
def parse_input(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    contact = Record(name)
    contact.add_phone(phone)
    
    if name not in book:
        book.add_record(contact)
        return "Contact added."
    else:
        return "Contact already exists."


# Щоб вже все було як в классах, добавляю функцію добавити номер.
@input_error
def add_number(args, book: AddressBook):
    name, number = args
    book.find_record(name).add_phone(number)
    return "Number added."

# Змінюю номер, але у нас в book список номерів, і метод edit_phone розрахований на
# ввід номеру, який слід змінити. Тому зробив так.
@input_error
def change_number(args, book: AddressBook):
    name, old_number, new_number = args
    if name in book:
        user = book.find_record(name)
        user.edit_phone(old_number, new_number)
        return 'Number changed.'
    return f"User '{name}' not found."


@input_error
def show_phone(user: tuple, book: AddressBook):
    for name, record in book.items():
        if user[0] == name:
            return record.show_phones()


def show_base(book: AddressBook):
    if not book:
        return "Book is empty."
    
    result = ""
    
    for name, record in book.items():
        result += f"{record}\n"
        
    return result


# При повторному вводі змінює дату
@input_error
def add_birthday(args, book: AddressBook):
    user_name, user_birthday = args
    for name, record in book.items():
        if user_name == name:
            record.add_birthday(user_birthday)
            return f"{args[0]}'s Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    return book.find_record(args[0]).birthday


commands = """
Commands:
    all;
    commands;
    add user number;
    add-number user;
    add-birthday user (format DD.MM.YYYY);
    show-birthday user;
    birthdays;
    phone user;
    change user old-number new-number;
    hello
    exit/quit/close
"""


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print(commands)
    while True:
        user_input = input("Enter a commands: ")
        command, *args = parse_input(user_input)

        if command in ['close', 'quit', 'exit']:
            print("Good bye!")
            break
        
        match command:
            case 'commands':
                print(commands)
            case 'hello':
                print("Hello im Jarvis! Im here for help you!")
            case 'all':
                print(show_base(book))
            case 'add':
                print(add_contact(args, book))
            case 'add-number':
                print(add_number(args,book))
            case 'add-birthday':
                print(add_birthday(args, book))
            case 'show-birthday':
                print(show_birthday(args, book))
            case 'birthdays':
                print(book.get_upcoming_birthdays())
            case 'phone':
                print(show_phone(args, book))
            case 'change':
                print(change_number(args, book))
            case _:
                print("Bad command.")

if __name__ == '__main__':
    main()
