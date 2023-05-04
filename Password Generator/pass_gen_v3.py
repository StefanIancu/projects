import random
from string import ascii_letters as alphabet
from string import digits 
from string import punctuation as symbols

all_characters = alphabet + digits + symbols
without_digits = alphabet + symbols
without_symbols = alphabet + digits

print("PASSWORD GENERATOR")
print("*" * 30)


def get_user_length():
    """Gets the user wanted password length."""
    return int(input("Password length: "))
        

def get_user_choice(prompt : str) -> bool: 
    while True:
        choice = input(prompt)
        if choice.lower() not in ("y", "n"):
            print("Not a valid answer. Please choose 'y' or 'n'!")
        else:
            return choice.lower() == "y"
    
def generate_digitless_password():
    """Returns a digitless password."""
    for i in range(get_user_length()):
        password = random.choice(without_digits)
        unique_password = "".join(dict.fromkeys(password))
        print(unique_password, end="")
        
def generate_symbless_password():
    """Returns a password without symbols."""
    for i in range(get_user_length()):
        password = random.choice(without_symbols)
        unique_password = "".join(dict.fromkeys(password))
        print(unique_password, end="")
    
    
def generate_alphabetical_password():
    """Returns a password containing just letters."""
    for i in range(get_user_length()):
        password = random.choice(alphabet)
        unique_password = "".join(dict.fromkeys(password))
        print(unique_password, end="")
    
    
def generate_full_password():
    """Returns a password with all characters."""
    for i in range(get_user_length()):
        password = random.choice(all_characters)
        unique_password = "".join(dict.fromkeys(password))
        print(unique_password, end="")
        
        
def pass_gen():
    """Returns the final password for the user based on their preferences."""
    if get_user_choice("Digits? [y/n]"):
        if get_user_choice("Symbols? [y/n]"):
            generate_full_password()
        else:
            generate_symbless_password()
    else:
        if get_user_choice("Symbols? [y/n]"):
            generate_digitless_password()
        else: 
            generate_alphabetical_password()

pass_gen()


