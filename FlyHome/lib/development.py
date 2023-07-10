import csv
import random
import sqlite3
import json
import os
import getpass
import logging
import smtplib
import sys

from hashlib import blake2b
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from pathlib import Path
from string import ascii_uppercase, punctuation
from datetime import datetime
from time import strftime


from fpdf import FPDF

# paths to certain dirs
ROOT = Path(__file__).parent
DB_PATH = ROOT / "flights.db"
UTILS = ROOT.parent / "utils"
TICKETS = ROOT.parent / "tickets"
DATA_STORE_PATH = ROOT / "count.json"
USER_PATH = ROOT / "user.json"

# establishing a database connection
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# any destination/its price can be changed from here. always change the 
# key - destination using lowercase and the value - price needs to be an integer/float
DESTINATIONS_AND_PRICES = {
    "timisoara": 150,
    "budapest": 150,
    "bratislava": 165,
    "sofia": 150,
    "prague": 200,
    "berlin": 250,
    "rome": 400,
    "paris": 350,
    "basel": 550,
    "tokyo": 999,
}

# "now" variable is used to input the date (month, year) on the ticket. the default
# will always be the present month/year
now = date.today()
DATE = strftime("%m.%y")

# "FROM" constant stands for the departure location, can be changed anytime
FROM = "Bucharest OTP"

# global variable - stores the input of get_user_destination in order to pass it 
# to read_numbers method. this lets the user choose only from the flights that are 
# currently displaying on the screen
destination_global = ""

# a user needs to provide information such as a name, a preferred location with a
# preferred flight number (for default, there are three flights per location, each
# at different time - each flight has a unique number)
# once they've picked a flight to a specific location, they could choose if they
# would like to book a specific seat or register their luggage (the final cost
# of the ticket will increase)
# *the starting price matches the price from the "DESTINATIONS AND PRICES" dictionary
# and increases based on their choices
# in the end, they will choose a departure date from the present month and their
# boarding pass will be generated as a PDF file in the "tickets" dir.

# dict containing user ids and passwords
staff_accounts = { "stefan.iancu": "12345",
                  "andrei.stancu" : "6789"
}

# logging config to store useful information 
logging.basicConfig(filename=f"{UTILS}/log.log", level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s")

# credentials for the smtp server and email
EMAIL_PASS = "fshbrcqyywpavsbd"
EMAIL_USER = "pythontest.odyssey2001@gmail.com"
EMAIL_SERVER = "smtp.gmail.com"
EMAIL_SERVER_PORT = 465

# symbols 
db_not_check_in = "❌"
db_check_in = "✅"

# creating a class for each menu option. each class has certain methods that
# work together (doc-string can be found for each method)


class BookFlight:
    current_price = 0
    
    def __init__(self, title):
        self.__title = title

    @property
    def title(self):
        return self.__title

    def get_user_name(self):
        """Takes the user's name."""
        while True:
            name_answer = input("What is your name?")
            if any(i.isdigit() for i in name_answer):
                print("Please enter the correct name without numbers.")
            elif any(i for i in name_answer if i in punctuation):
                print("Please don't use characters.")
            elif name_answer == "":
                print("Field required.")
            elif name_answer.isspace():
                print("Field required.")
            else:
                break
        print(f"Welcome, {name_answer.title()}!")
        return name_answer.title()

    def get_user_destination(self):
        """Takes the user destination and matches the starting price of the
        ticket with the specific destination price from DESTINATIONS_AND_PRICES
        dictionary. This can be changed anytime."""
        global destination_global
        while True:
            destination_answer = input(f"Where would you like to go? ")
            if destination_answer.lower() in list(DESTINATIONS_AND_PRICES.keys()):
                PlaneTicket.current_price += DESTINATIONS_AND_PRICES[
                    destination_answer.lower()
                ]
                develop_data_object.read_flights(destination_answer)
                break
            else:
                print("We are sorry. We currently don't fly there!")
        destination_global = destination_answer.title()
        return destination_answer

# checking if the flight exists and if there are any available seats. lets
# the user only choose from the flights matched with the destination they previously
# chose
    def pick_a_flight(self):
        """Asks the user to pick a flight number from the list of available
        flights."""
        while True:
            flight_answer = input("Please choose a flight by entering its number: ")
            if develop_data_object.read_numbers(flight_answer.upper(), destination_global):
                if not develop_data_object.check_seats(flight_answer.upper()):
                    break
                else:
                    print("No seats left for this flight. Please choose another.")
            else:
                print("Please enter the correct flight number.")
        return flight_answer

    def get_user_seat(self):
        """Asks the user if they would like to book a seat or not. If the user
        replies positively, the current price will increase."""
        while True:
            seat_answer = input("Would you like to reserve a seat? [y/n]")
            if seat_answer == "":
                print("Field required.")
            elif seat_answer in "yesYES":
                if seat_answer not in "eE":
                    PlaneTicket.current_price += 50
                    seat_answer = (
                        f"{random.choice(range(75))}{random.choice(ascii_uppercase)}"
                    )
                    print("Seat reserved!")
                    break
                else:
                    print("Sorry, that's not an answer.")
            elif seat_answer in "noNO":
                if seat_answer not in "oO":
                    seat_answer = "(to be assigned at check-in)"
                    break
                else:
                    print("Sorry, that's not an answer.")
            else:
                print("Sorry, not an answer.")
        return seat_answer

    def get_user_luggage(self):
        """Asks the user if they would like to book a luggage. If the user
        replies positively, the current price will increase."""
        while True:
            luggage_answer = input("Would you like to book a luggage? [y/n]")
            if luggage_answer == "":
                print("Field required.")
            elif luggage_answer in "yesYES":
                if luggage_answer not in "eE":
                    PlaneTicket.current_price += 50
                    print("Luggage registered!")
                    luggage_answer = "Booked"
                    break
                else:
                    print("Sorry, that's not an answer.")
            elif luggage_answer in "noNO":
                if luggage_answer not in "oO":
                    luggage_answer = "Unbooked"
                    break
                else:
                    print("Sorry, that's not an answer.")
            else:
                print("Sorry, that's not an answer.")
        return luggage_answer

    def get_user_date(self):
        """Asks the user the date (day) when they would like to fly.
        This is combined with the DATE constant which is the current month of
        the year - based on real date&time."""
        while True:
            user_date = input(f"When would you like to fly? [day.{DATE}]")
            if user_date.isdigit():
                user_date = int(user_date)
                if 0 < user_date <= 31:
                    if check.check_date(user_date):
                        break
                    else:
                        print("Cannot choose a date from past.")
                else:
                    print("Date must be between 1 and 31.")
            else:
                print("Please enter a valid format [day].")
        return user_date

    def generate_ticket(self):
        """Main method that takes all the information together and generates
        an object - ticket. It also adds the ticket's number to the "flights"
        database."""
        # setting the current price to 0
        PlaneTicket.current_price = 0
        name = self.get_user_name()
        WhereToGo.see_list_of_destinations()
        destination = self.get_user_destination()
        flight = self.pick_a_flight()
        seat = self.get_user_seat()
        luggage = self.get_user_luggage()
        date = self.get_user_date()
        departure_time, gate = develop_data_object.read_dep_time(flight.upper())
        price = PlaneTicket.current_price
        print("Your ticket has been generated. Thank you for picking us!")
        develop_data_object.drop_seats(flight.upper())
        # ticket = PlaneTicket(PlaneTicket.number, name, seat, date, destination, flight, gate)
        # number = ticket.number
        number = f"{random.choice(ascii_uppercase)}{load_json()}"
        number_json = load_json()
        save_json(number_json)
        self.generate_pdf(
            number, seat, name, destination, date, flight, departure_time, gate
        )
        # updating the database with the information from the user
        develop_data_object.update_db(name, destination, price, number, flight, gate, date)
        logging.info("Ticket generated.")
        if check_email():
            send_email(name, number, date, price, seat, luggage, destination.title(), flight)
            logging.info("Email sent.")
            print("Your ticket has been sent.")

    def generate_pdf(
        self, number, seat, name, destination, date, flight_number, departure_time, gate
    ):
        """Method that takes some user information and fills a PDF file
        with the specific information."""
        create_destination_dir(destination, flight_number)
        pdf = FPDF()
        pdf.add_page(orientation="l")
        pdf.set_font("Arial", size=15)
        pdf.cell(40, 10, border=1, txt=f"Ticket no: {number} ", ln=1)
        pdf.cell(270, 10, txt="FlyHome", ln=1, align="R")
        pdf.cell(250, 20, txt="BOARDING PASS", ln=2, align="C")

        pdf.cell(52, 10, txt=f"Mr./Mrs. {name} ", ln=3, align="L")
        pdf.cell(150, 10, txt=f"Seat number: {seat}", ln=4, align="L")
        pdf.cell(
            150, 10, txt=f"Flight number: {flight_number.upper()}", ln=4, align="L"
        )

        pdf.cell(270, 10, txt=f"Departure time: {departure_time}", ln=7, align="R")
        pdf.cell(270, 10, txt=f"Departure date: {date}.{DATE}", ln=7, align="R")
        pdf.cell(270, 10, txt=f"Gate: {gate}", ln=8, align="R")
        pdf.cell(270, 10, txt=f"From: {FROM}", ln=9, align="R")
        pdf.cell(270, 10, txt=f"To: {destination.title()}", ln=10, align="R")
        pdf.image(f"{UTILS}/airplane.jpeg", w=10, h=10, x=235, y=120)

        pdf.cell(
            100, 10, txt="Gate closes 15 minutes before departure.", ln=11, align="L"
        )
        pdf.cell(
            100, 10, txt="Thank you for choosing to fly with us!", ln=12, align="L"
        )
        pdf.cell(100, 10, txt="More details at: www.flyhome.com", ln=13, align="L")

        pdf.image(f"{UTILS}/plane.jpeg", w=60, h=60, x=190, y=1)
        pdf.code39("*fpdf2*", x=130, y=140, w=4, h=15)

        pdf.cell(
            100, 10, txt="*Please watch screens for border time.", ln=21, align="L"
        )
        pdf.cell(100, 10, txt="**No refund available for this flight.", ln=22, align="")

        pdf.output(f"{TICKETS}/{destination.title()}/{flight_number.upper()}/planeticket_{number}.pdf")


# the user has the option to see the destinations and their starting prices
# without booking a flight. usually read from a csv or xls file.


class WhereToGo:
    def __init__(self, title):
        self.__title = title

    @property
    def title(self):
        return self.__title

    @staticmethod
    def see_list_of_destinations():
        """Reads the destinations available and their prices from a csv file."""
        with open(f"{UTILS}/destinations.csv") as fin:
            reader = csv.reader(fin.readlines()[1:])

        for line in reader:
            print(f"""{line[0].replace(";", " from €")}""")


# the user has the option to see the help option. here could be anything from
# flight-related details to traveling tips. usually read from a doc, txt file.
# for default there is a guide related to EU traveling rights.


class Help:
    def __init__(self, title):
        self.__title = title

    @property
    def title(self):
        return self.__title

    @staticmethod
    def ask_help():
        """Provides useful information to the user."""
        with open(f"{UTILS}/travel.txt", "r") as fin:
            content = fin.readlines()

        for line in content:
            if line.isspace():
                continue
            else:
                print(line.strip(" \n\r\t"))


# the user has the option to cancel a reservation by inputting the ticket number
# received when first booked.
# when a reservation is deleted, the "seat available" value returns to the previous value
# and the pdf generated is deleted


class CancelFlight:
    def __init__(self, title):
        self.__title = title

    @property
    def title(self):
        return self.__title

    @staticmethod
    def delete_reservation():
        """Deletes a reservation booked by the user."""
        while True:
            del_res = input(
                "Please enter your ticket number to delete the reservation: "
            )
            if develop_data_object.get_ticket_existence(del_res.upper()):
                develop_data_object.undo_seats(del_res.upper())
                cursor.execute(
                    """DELETE FROM flights WHERE ticket == ?""", (del_res.upper(),)
                )
                connection.commit()
                logging.warning("Reservation deleted.")
                try:
                    del_file(f"planeticket_{del_res.upper()}.pdf")
                except OSError as err:
                    print(err)
                else:    
                    print(
                     f"The reservation with {del_res.upper()} has been successfully deleted. "
                    )
                break
            else:
                print(f"Ticket {del_res.upper()} doesn't exist.")


# class that defines the attributes of a plane ticket


class PlaneTicket(BookFlight):
    current_number = 100

    def __init__(self, number, name: str, seat, date, destination, flight_number, gate):
        self.__number = f"{random.choice(ascii_uppercase)}{PlaneTicket.current_number}"
        self.__name = name
        self.__seat = seat
        self.__date = date
        self.__destination = destination
        self.__flight_number = flight_number
        self.__gate = gate
        PlaneTicket.current_number += 1
        self.current_price = 0

    @property
    def name(self):
        return str(self.__name)

    @property
    def number(self):
        return self.__number

    @property
    def seat(self):
        return self.__seat

    @property
    def date(self):
        return self.__date

    @property
    def flight_number(self):
        return self.__flight_number

    @property
    def gate(self):
        return self.__gate
    
    @property
    def destination(self):
        if self.__destination not in list(DESTINATIONS_AND_PRICES.keys()):
            print(f"Destination not in {DESTINATIONS_AND_PRICES}.")
        return self.__destination


# this Database class has only methods that are operating on the local sql database.
# either to select info, update, delete, check if exists and a method for the staff
# where they can record new flights
# each method is used together with other methods from above in order to make the
# program run accurately


class Database(BookFlight):
    def __init__(self, path: Path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def update_db(self, name, destination, price, number, flight, gate, flight_date):
        """Method that updates the flights database with all the information from the user."""
        with open(USER_PATH, "r") as fin:
            user = json.load(fin)
        self.cursor.execute(
            """INSERT INTO flights ("name", "destination", "cost", "ticket", "flight_nr", "gate", "user", "date", "check_in") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, destination.title(), price, number, flight.upper(), gate, user, f"{flight_date}.{DATE}", db_not_check_in)
        )
        self.connection.commit()

    def read_database(self):
        """Method that shows the booked flights."""
        with open(USER_PATH,  "r") as fin:
            user = json.load(fin)
        rows = self.cursor.execute(
            """SELECT "name", "destination", "cost", "ticket", "flight_nr", "gate", "date", "check_in" FROM flights
            where user ==?""", (user,))
        for row in rows:
            name, destination, cost, ticket, flight, gate, flight_date, check_in = row
            print(
                f"{name}, {FROM}->{destination}, €{cost}, ticket no.{ticket}, flight number {flight}, gate {gate} on {flight_date} | {check_in}"
            )

# staff only
    def add_flight(self):
        """Method that adds a flight to the "flights" database containing
        destination, flight number, departure time and number of seats left
        - FOR STAFF ONLY."""
        destination = input("Destination: ")
        flight_number = input("Flight number: ")
        time = input("Departure time: ")
        seats = input("Number of seats: ")
        gate = input("Gate number: ")
        self.cursor.execute(
            """INSERT INTO departures ("destination", "flight_number", "time", "seats ", "gate") VALUES (?, ?, ?, ?, ?)""",
            (destination.title(), flight_number, time, seats, gate),
        )
        self.connection.commit()
        logging.info("New flight added.")

    def read_flights(self, destination):
        """Method that reads from a database of flights a specific destination
        which the user chooses - method for "BOOK A FLIGHT OPTION" where it
        needs an argument - user input."""
        while True:
            if destination.lower() in DESTINATIONS_AND_PRICES.keys():
                rows = self.cursor.execute(
                    """SELECT * FROM departures WHERE "destination" is ?""",
                    (destination.title(),),
                )
                break
            else:
                print(
                    "We currently don't fly there. Please see our list of destinations."
                )
                WhereToGo.see_list_of_destinations()

        print(f"Upcoming flights for {destination.title()}:")
        for row in rows:
            dest, flight_nr, dep_time, seats, gate = row
            print(
                f"{FROM}-> {dest}, flight number {flight_nr}, departure at {dep_time}, available seats {seats}, gate {gate}."
            )

    def read_flights_for_available(self):
        """Method that reads from a database of flights a specific destination
        which the user chooses - method for "AVAILABLE FLIGHTS" option where it
        is static, doesn't need any arguments."""
        while True:
            destination = input("What destination interests you? ")
            if destination.lower() in DESTINATIONS_AND_PRICES.keys():
                rows = self.cursor.execute(
                    """SELECT * FROM departures WHERE "destination" is ?""",
                    (destination.title(),),
                )
                break
            else:
                print(
                    "We currently don't fly there. Please see our list of destinations."
                )
                WhereToGo.see_list_of_destinations()

        print(f"Upcoming flights for {destination.title()}:")
        for row in rows:
            dest, flight_nr, dep_time, seats, gate = row
            print(
                f"{FROM}-> {dest}, flight number {flight_nr}, departure at {dep_time}, available seats {seats}, gate {gate}."
            )

    def read_numbers(self, flight_number, destination):
        """Method that checks from the database "flights" that certain flights 
        numbers are actually existing."""
        rows = self.cursor.execute(
            """SELECT EXISTS(SELECT 1 FROM departures WHERE flight_number = ? and destination = ?)""",
            (flight_number.upper(), destination),
        )

        for row in rows:
            return row[0] == 1

    def get_ticket_existence(self, ticket):
        """Method that returns bool if a specific ticket is in flights database
        in order to help the delete_reservation method to be accurate."""
        rows = self.cursor.execute(
            """SELECT EXISTS(SELECT 1 FROM flights WHERE ticket = ?)""",
            (ticket.upper(),),
        )

        for row in rows:
            return row[0] == 1

# two methods that are taking care of the seats value to be constantly updating
    def drop_seats(self, flight_number):
        """ "Method that substitutes one seat for each booking in order to keep
        the "available seats" value updated."""
        self.cursor.execute(
            """UPDATE departures 
            SET "seats " = "seats " - 1 
            WHERE "flight_number" == ? """,
            (flight_number,),
        )
        self.connection.commit()

    def undo_seats(self, ticket_number):
        """Method that adds one seat for each deleted booking in order to keep
        the "available seats" value updated."""
        self.cursor.execute(
            """UPDATE departures
            SET "seats " = "seats " + 1 
            WHERE flight_number IN (
            SELECT flight_nr
            FROM flights
            WHERE ticket == ?
            );
            """,
            (ticket_number,),
        )
        self.connection.commit()

# each flight has his own gate number
    def read_dep_time(self, flight_number: str) -> tuple: # type: ignore
        """Method that returns the departure time of a specific flight."""
        rows = self.cursor.execute(
            """SELECT time, gate FROM departures WHERE flight_number == ? 
            """,
            (flight_number,),
        )
        for row in rows:
            time, gate = row
            return time, gate
        
    def return_time_of_flight(self, flight_number: str) -> tuple: # type: ignore
        """Method that returns the departure time of a specific flight."""
        rows = self.cursor.execute(
            """SELECT time FROM departures WHERE flight_number == ? 
            """,
            (flight_number,),
        )
        for row in rows:
            time = row
            return time[0]

    def update_check_in(self, ticket_number):
        """Method that updates the status of a check-in once it is completed."""
        rows = self.cursor.execute(
            """UPDATE flights SET check_in = ? WHERE ticket == ?""",
            (db_check_in, ticket_number)
            )
        self.connection.commit()

    def verify_check_in(self, ticket_number):
        """Method that returns a bool if a check-in if it's already made."""
        rows = self.cursor.execute(
            """SELECT EXISTS(SELECT 1 FROM flights WHERE check_in == ? and ticket ==?)""",
            (db_check_in, ticket_number)
        )
        for row in rows:
            return row[0] == 1

# a while loop + this method should not let the user advance if there are 0 seats
    def check_seats(self, flight_number):
        """Method that returns a bool if a certain flight has no seat
        available."""
        rows = self.cursor.execute(
            """SELECT EXISTS (SELECT 1 FROM departures WHERE "seats " == 0 and
            "flight_number" == ?)""", (flight_number, )
        )

        for row in rows:
            return row[0] == 1
        
    def check_flight_date(self, ticket_number):
        """Method that returns the date of a specific flight."""
        rows = self.cursor.execute("""SELECT "date" from flights where "ticket" == ?""",
                                   (ticket_number, ))
        for row in rows:
            flight_date = row[0]
            return flight_date

# check tickets stats
    @staticmethod
    def check_cost_stats(destination=None):
        """Method that returns the number of bought tickets, the average cost 
        of a ticket and the sum of all tickets that have been bought - FOR STAFF ONLY.
        *optional argument - destination"""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        if destination != None:
            rows = cursor.execute(
                """SELECT count(ticket), avg(cost), sum(cost)from flights WHERE destination == ?""",
                (destination.title(), )
            )
            for row in rows:
                number1, avg1, sum1 = row
                print(f"Total number of purchased tickets for {destination.title()} is {number1}.") 
                print(f"The average cost is {round(avg1)}€.")
                print(f"Income generated {sum1}€.")
                print("-" * 50)
        else:
            rows = cursor.execute(
                """SELECT count(ticket), avg(cost), sum(cost)from flights"""
            )
            for row in rows:
                number, avg, sum = row
                print(f"Total number of purchased tickets: {number}.")
                print(f"The average cost is {round(avg)}€.")
                print(f"Income generated {sum}€.")
                print("-" * 50)
        
# check flights stats
    @staticmethod
    def check_flights_stats(destination=None):
        """Method that returns the average number of available seats and the total of seats 
        -FOR STAFF ONLY. 
        *optional argument - destination"""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        if destination != None:
            rows = cursor.execute(
                """SELECT avg("seats "), sum("seats ") from departures WHERE destination == ?""",
                (destination.title(), )
            )
            for row in rows:
                avg_seats, total_seats = row
                print(f"The total numbers of seats left for {destination.title()} is {total_seats}.")
                print(f"The average number of seats is {round(avg_seats)} per flight.")
                print("-" * 50)
        else:
            rows = cursor.execute(
                """SELECT avg("seats "), sum("seats ") from departures"""
            )
            for row in rows:
                average, total = row
                print(f"The total numbers of available seats is {total}.")
                print(f"The average number of seats is {round(average)} per flight.")
                print("-" * 50)

develop_data_object = Database(DB_PATH)


class User:

    def __init__(self, category):
        self.__category = category

    @property
    def category(self):
        return self.__category
    
    def user_signup(self):
        """Takes the user through the registration process. Doesn't let the user choose
        a username that already exists"""
        while True:
            username = input("Please choose an username: ")
            if self.check_username(username):
                print("Username already exists. Please choose another.")
            else:
                break
        password = getpass.getpass("Please choose a password: ")
        confirmed_password = getpass.getpass("Please confirm your password: ")

        if confirmed_password == password:
            encode = blake2b(digest_size=15)
            hash = confirmed_password.encode()
            updated = encode.update(hash)
            final = encode.hexdigest()
            
            cursor.execute("""INSERT INTO users ("username", "password") VALUES (?, ?)""",
                        (username, final))
            connection.commit()
            print("Registered successful - redirected to the login screen.")
            logging.info(f"{username} registered.")
        else:
            print("Passwords don't match.")

    def user_authenticate(self):
        """Takes the user through the authentication process and stores the username
        in a temporary json file in order to use it to display info only for that user."""
        while True:
            username = input("Please enter your username: ")
            password = getpass.getpass("Please enter your password: ")
            encode = blake2b(digest_size=15)
            hash = password.encode()
            updated = encode.update(hash)
            final = encode.hexdigest()
            if self.check_passwords(username, final):
                print("Access granted.")
                logging.info(f"{username} logged in.")
                try:
                    with open(USER_PATH, "w") as fout:
                        json.dump(username, fout, indent=4)
                except OSError as err:
                    print(err)
                break
            else:
                print("Access denied.")
    
    def check_passwords(self, username, password):
        """Check if the credentials are matching."""
        rows = cursor.execute("""SELECT EXISTS(SELECT 1 FROM users where "username" == ? and "password" == ?)""",
                       (username, password))
        
        for row in rows:
            return row[0] == 1
        
    def check_username(self, username):
        """Checks if the chose username exists or not."""
        rows = cursor.execute("""SELECT EXISTS(SELECT 1 FROM users where "username" == ?)""",
                       (username, ))

        for row in rows:
            return row[0] == 1
        
    def login_menu(self):
        """Prints the login menu in a while loop."""
        while True:
            print("{:-^50}".format("FlyHome"))
            print("We take you back home...or pretty far away from it!")
            print("")
            print("1 - Log in")
            print("2 - Sign-up")
            print("3 - Quick check-in")
            print("4 - Staff only")
            print("5 - Exit")
            choice = input("Please choose an item from the list: ")
            if choice == "1":
                self.user_authenticate()
                break
            elif choice == "2":
                self.user_signup()
                self.user_authenticate()
                break
            elif choice == "3":
                self.user_authenticate()
                check.self_check_in()
                break
            elif choice == "4":
                staff_only()
            elif choice == "5":
                sys.exit(0)
            else:
                print("Please choose an item within the range above.")


# defined three json functions: 
# save_json is overwriting the json.count file with the current ticket number
# load_json is returning the count value and adds +1 to it 
# reset_json is resetting the counter from a desired value
def save_json(number):
    with open(DATA_STORE_PATH, "w") as fout:
        json.dump(number, fout, indent=4)

def load_json():
    with open(DATA_STORE_PATH, "r") as fin:
        count = json.load(fin)
        return count + 1

def reset_json():
    number = int(input("Choose a value to restart the counter: "))
    with open(DATA_STORE_PATH, "w") as fout:
        json.dump(number, fout, indent=4)
        print("Done - counter has been reset.")

# function that deletes the pdf file generated after the reservation has been 
# cancelled
def del_file(ticket: str):
    for dirpath, dir, files in os.walk(TICKETS):
        for _file in files:
            if _file == ticket:  
                os.remove(os.path.join(dirpath, _file))
                print("File deleted.")

# function that takes the staff-user through the authentication process
def authenticate():
    """Asks the staff-user for a password and username in order to access the 
    "Staff only" secondary menu."""
    while True:
        username = input("Please enter your staff-username: ")
        if username in list(staff_accounts.keys()):
            password = getpass.getpass("Please enter your staff-password: ")
            if password == staff_accounts.get(username):
                print("Access granted.")
                logging.info(f"{username} connected - STAFF.")
                break
            else:
                print("Access denied - please try again.")
        else:
            print("Staff-user not found.")

# sub-menu for the "Staff only" option in main
def staff_option_one():
    """Method for the "Staff only" screen that represents the first option. 
    Works based on the database and returns flight statistics for the staff."""
    while True:
            print("{:-^50}".format("Flight stats"))
            print("1 - General flight statistics")
            print("2 - Particular flight statistics")
            reports1 = input("Choose an option: ")
            if reports1 == "1":
                print("{:-^50}".format("General flight stats"))
                print(f"{now}")
                Database.check_flights_stats()
                if input("Press any to go back: "):
                    break
                break
            if reports1 == "2":
                answer = input("Choose a destination: ")
                if answer.lower() in list(DESTINATIONS_AND_PRICES.keys()):
                    print("{:-^50}".format("Particular flight stats"))
                    print(f"{now}")
                    Database.check_flights_stats(answer)
                    if input("Press any to go back: "):
                        break
                    break
            elif any(i for i in reports1 if i in punctuation):
                print("No characters allowed.")
            else:
                print("Not an answer.")

#sub-menu for "Staff only" option in main
def staff_option_two():
    """Method for the "Staff only" screen that represents the second option. 
    Works based on the database and returns ticket statistics for the staff."""
    while True:
            print("{:-^50}".format("Ticket stats"))
            print("1 - General ticket statistics")
            print("2 - Particular ticket statistics")
            reports1 = input("Choose an option: ")
            if reports1 == "1":
                print("{:-^50}".format("General ticket stats"))
                print(f"{now}")
                Database.check_cost_stats()
                if input("Press any to go back: "):
                    break
                break   
            if reports1 == "2":
                answer = input("Choose a destination: ")
                if answer.lower() in list(DESTINATIONS_AND_PRICES.keys()):
                    print("{:-^50}".format("Particular ticket stats"))
                    print(f"{now}")
                    Database.check_cost_stats(answer)
                    if input("Press any to go back: "):
                        break
                    break
            if any(i for i in reports1 if i in punctuation):
                print("No characters allowed.")
            else:
                print("Not an answer.")


# sends the generated ticket via email to the user
def send_email(user_name, ticket, date, price, seat, luggage, destination, flight_number):
    """Stores a html template, fills it with certain arguments and sends the 
    email to the user along with the boarding pass generated - if desired."""

    user_email = input("Let us know your email so we can forward your boarding pass: ")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your reservation at FlyHome"
    message["From"] = EMAIL_USER
    message["To"] = user_email

    html_base = f"""
    <html>
    <body>
        <h2>Hello {user_name},</h2>
        <h3>You will find your boarding pass attached below. See you on board soon!</h3>

        <p>Please try to arrive at the gate with a minimum of two hours before boarding.</p>
        <p>Have both your boarding pass out and a form of ID - either your driver's license or your passport (it must be your passport if you're heading out of the country) - readily available.</p>
        <p>A TSA agent will check your boarding pass to your ID, and then you must successfully pass through the security check.</p>

        <p>*First class always boards the plane first, followed by business class and people with disabilities or infants.</p>
        <p>In case you didn't reserve a seat, one will be automatically assigned at the check-in.</p>

        <h4>RESERVATION SUMMARY</h4>
        <ul>
        <li>Destination........{destination}</li>
        <li>Date.........{date}.{DATE}</li>
        <li>Seat.........{seat}</li>
        <li>Luggage......{luggage}</li>
        <li><b>TOTAL.........€{price}</b></li>
        </ul>

        <p>For any details regarding the reservation please email us at support@flyhome.com</p>
        <p>Have the best flight,</p>
        <p>FlyHome Team</p>
    </body>
    </html>
    """
    
    part2 = MIMEText(html_base, "html")

    ticket_path = f"{TICKETS}/{destination.title()}/{flight_number.upper()}/planeticket_{ticket}.pdf"

    with open(ticket_path, "rb") as fin:
        opened_ticket = fin.read()
    
    attached_file = MIMEApplication(opened_ticket, _subtype = "pdf")
    attached_file.add_header("content-disposition", "attachment", filename=f"planeticket_{ticket.upper()}.pdf")

    message.attach(part2)
    message.attach(attached_file)

    server = smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_SERVER_PORT)
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, user_email, message.as_string())

# returns the user's preference to get the pdf on email or not
def check_email() -> bool:
    """Asks the user if they want to receive the boarding pass on email."""
    while True: 
        ask_email = input("Would you like to receive the boarding pass on email? [y/n]")
        if ask_email in "yesYES":
            if ask_email not in "eEsS":
                return True
            else:
                print("That's not an answer.")
        elif ask_email in "noNO":
            if ask_email not in "oO":
                print("Got it, we won't bother you.")
                return False
            else:
                print("That's not an answer.")
        else:
            print("Please input the correct answer.")

# creates a dir for every flight and destination for a better management of tickets
def create_destination_dir(destination, flight_number):
    folder_path = TICKETS / f"{destination.title()}" / f"{flight_number.upper()}"
    try:
        folder_path.mkdir(exist_ok=True, parents=True)
    except OSError as err:
        print(err)
            

class CheckIn:

    def __init__(self, title):
        self.__title = title

    @property
    def title(self):
        return self.__title
    
#lets the user to check-in his flight
    def self_check_in(self):
        """Method that compares the flight-date with the current date in order
        to establish if there are less than 24h to the flight. If True, check-in 
        will proceed. Otherwise, check-in would be locked."""
        develop_data_object.read_database()
        print("-" * 62)
        print("NOTE: Check-in only available 24h or less before flight time. ")
        while True:
            ticket = input("Enter ticket number for check-in: ")
            if develop_data_object.get_ticket_existence(ticket.upper()):
                date_flight = develop_data_object.check_flight_date(ticket.upper())
                flight = input("Please confirm your flight number: ")
                if check.check_date(date_flight, flight.upper()):
                    if not develop_data_object.verify_check_in(ticket.upper()):
                        develop_data_object.update_check_in(ticket.upper())
                        print("Check-in successfully!")
                        break
                    else:
                        print(f"Check-in already made for ticket {ticket.upper()}.")
            else:
                print(f"Ticket {ticket} doesn't exist.")

    def check_date(self, day=None, flight=None):
        """Method that checks if a certain date is present-future available and 
        doesn't let the user to advance if the date it's in the past. """
        if day == None:
            day = int(input("Choose a date: "))

        if flight != None:
            present_time = strftime("%d.%m.%y, %H:%M")
            start_time = datetime.strptime(present_time, "%d.%m.%y, %H:%M")
            departure_time = develop_data_object.return_time_of_flight(flight)
            end_time = datetime.strptime(f"{day}, {departure_time}", "%d.%m.%y, %H:%M")

            delta = end_time - start_time
            sec = delta.total_seconds()
            hours = sec / (60 * 60)

            if hours > 24:
                print(f"Check-in closed. {round(hours)} hours to your flight.")
                return False
            elif hours < 0:
                print(f"Cannot check-in for a past flight.")
                return False
            elif hours <= 24:
                return True
        else:
            present_time = strftime("%d.%m.%y")
            start_time = datetime.strptime(present_time, "%d.%m.%y")
            compare_time = datetime.strptime(f"{day}.{DATE}", "%d.%m.%y")

            delta = compare_time - start_time
            sec = delta.total_seconds()
            hours = sec / (60 * 60)

            return True if hours >= 0 else False

check = CheckIn("title")

def staff_only():
    """Method that combines the two staff options and binds them together into 
    a sub-menu choice."""
    try:
        authenticate()
    except ValueError as err:
        print(err)
    else:
        while True:
            print("{:-^50}".format("Staff only"))
            print("1 - Flight stats")
            print("2 - Ticket stats")
            answer = input("Please choose an item from above: ")
            if answer == "1":
                staff_option_one()
                break
            if answer == "2":
                staff_option_two()
                break
            if any(i for i in answer if i in punctuation):
                print("No characters allowed.")
            else:
                print("Not an option.")

