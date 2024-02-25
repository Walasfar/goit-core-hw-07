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
    record = book.find(name)
    if not record:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    
    record.add_phone(phone)
    return "Phone added." # Це реально красиво!

# При повторному вводі змінює дату
@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    
    if not record:
        return 'User does not exist.'
    
    record.add_birthday(birthday)
    return f"{name}'s Birthday added."


@input_error
def change_number(args, book: AddressBook):
    name, old_number, new_number = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    
    record.edit_phone(old_number, new_number)
    return f"User '{name}' phone changed."


@input_error
def show_phone(args: tuple, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found"
    return '; '.join(str(phone) for phone in record.phones)


def show_all(book: AddressBook):
    if not book:
        return "Book is empty."
    return book


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    return record.birthday

@input_error
def show_birthdays(args, book: AddressBook):
    birthdays_string, birthdays_list = book.get_upcoming_birthdays()
    return birthdays_string


commands = """
Commands:
    all;
    commands;
    add user number;
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
                print(show_all(book))
            case 'add':
                print(add_contact(args, book))
            case 'add-birthday':
                print(add_birthday(args, book))
            case 'show-birthday':
                print(show_birthday(args, book))
            case 'birthdays':
                print(show_birthdays(args, book))
            case 'phone':
                print(show_phone(args, book))
            case 'change':
                print(change_number(args, book))
            case _:
                print("Bad command.")

if __name__ == '__main__':
    main()
