import sys
from abc import ABC, abstractmethod
from typing import List

from lib.development import (
    DATE,
    DB_PATH,
    User,
    CheckIn,
    BookFlight,
    CancelFlight,
    Database,
    Help,
    WhereToGo,
    authenticate,
    staff_option_two,
    staff_option_one
)



# the menu works in a continuous loop until the user decides to exit.
# the user can go back to the main menu by pressing any key
# there can be an unlimited number of menu options


# defining the menu structure
class MenuItem(ABC):
    def __init__(self, title):
        self.title = title

    @abstractmethod
    def execute(self):
        pass


class MenuActionItem(MenuItem):
    def __init__(self, title, ticket):
        super.__init__(title)
        self.ticket: BookFlight = ticket


# each execute method has a try-except mechanism for each menu option
# each method is printing the menu option and it's formatted the same
# some methods are using other methods (for eg to get information from the
# Database or to call certain methods from the other classes in "development")
# each method has an input "any key" that stands from the "back" button that returns
# the user to main menu


class FindPlane(MenuItem):
    def execute(self):
        print(f"{self.title:-^50}\n")
        try:
            demo.generate_ticket()
        except OSError as err:
            print(err)
        input("Press any key to return: ")


class MyFlights(MenuItem):
    def execute(self):
        print(f"{self.title:-^50}\n")
        try:
            database.read_database()
        except OSError as err:
            print(err)
        input("Press any key to return: ")


class AvailableFlights(MenuItem):
    def execute(self):
        print(f"{self.title:-^50}\n")
        print(f"NOTE: Please note that the following flights are for {DATE}.")
        WhereToGo.see_list_of_destinations()
        try:
            database.read_flights_for_available()
        except OSError as err:
            print(err)
        input("Press any key to return: ")


class TravelTo(MenuItem):
    def execute(self):
        print(f"{self.title:-^50}\n")
        try:
            WhereToGo.see_list_of_destinations()
        except OSError as err:
            print(err)
        input("Press any key to return.")


class GiveHelp(MenuItem):
    def execute(self):
        print(f"{self.title:-^50}\n")
        try:
            Help.ask_help()
        except OSError as err:
            print(err)
        input("Press any key to return.")


class DelFlight(MenuItem):
    def execute(self):
        print(f"{self.title:-^50}\n")
        database.read_database()
        try:
            CancelFlight.delete_reservation()
        except OSError as err:
            print(err)
        input("Press any key to return.")

class UserCheckIn(MenuItem):
    def execute(self):
        print(f"{self.title:-^50}\n")
        try:
            check1.self_check_in()
        except OSError as err:
            print(err)
        input("Press any key to return.")

class MenuUserChoice(MenuItem):
    def __init__(self, title) -> None:
        super().__init__(title)
        self.__commands: List[MenuItem] = []

    def execute(self):
        user_choice = -1
        print(f"{self.title:-^50}")

        while user_choice not in range(1, len(self.__commands) + 1):
            for i, command in enumerate(self.__commands, start=1):
                print(f"{i} - {command.title}")
            try:
                user_choice = int(input("Please choose an item from the list: "))
            except ValueError:
                print("Please choose an item within the range above.")

        self.__commands[user_choice - 1].execute()

    def add_choice(self, choice: MenuItem) -> None:
        self.__commands.append(choice)


class ExitItem(MenuItem):
    def execute(self):
        print("Logged out.")
        sys.exit(0)


# created a demo object type BookFlight in order to access the "generate ticket" method
demo = BookFlight("demo")

# created demo object type Database to access certain methods from the class
database = Database(DB_PATH)

# created a demo object type User to access methods from the class
user = User("human")

#created a demo object type CheckIn to access methods the class
check1 = CheckIn("test")

# here are all the menu options. their names can be changed anytime as long as
# they're strings
main_menu = MenuUserChoice(f"Welcome to FlyHome!")
main_menu.add_choice(FindPlane("Book a flight"))
main_menu.add_choice(AvailableFlights("Available flights"))
main_menu.add_choice(MyFlights("See your reservations"))
main_menu.add_choice(DelFlight("Delete a reservation"))
main_menu.add_choice(TravelTo("Where to travel"))
main_menu.add_choice(GiveHelp("Get help"))
main_menu.add_choice(UserCheckIn("Check-in"))
main_menu.add_choice(ExitItem("Log out"))


# continuous execution until the user decides to exit the program
user.login_menu()
while True:
    main_menu.execute()