## FlyHome - CLI app that generates a boarding pass

### Stack + OS
VSCode, SQLite, Pyhton 3.11 /
Apple M1, Ventura 13.4.1

### Purpose

<li>To generate a boarding pass using the user data</li>
<li>To fix the problem of storing the user data safely</li>
<li>To help the staff monitor the flights, tickets and provide reports</li>

### Overlook 

<img width="552" alt="Screenshot 2023-07-10 at 11 17 42" src="https://github.com/StefanIancu/projects/assets/124818078/51c8a955-fe82-4ebf-b6b7-dba70e1f72f1">

### Structure 

<img width="231" alt="Screenshot 2023-07-10 at 11 38 13" src="https://github.com/StefanIancu/projects/assets/124818078/2a1fafac-ba7a-4843-8d4c-eb77a0df1074">

### First touch

<img width="406" alt="Screenshot 2023-07-10 at 11 15 18" src="https://github.com/StefanIancu/projects/assets/124818078/336b635f-1a61-46f5-9982-cc52bb3675bf">

This is the first menu or the login menu. The user has multiple choices like creating an account, using an existing account and checking-in an existing flight. 

There's also the "staff only" option which requires a special username and password that are given separately to each member of the staff. 

### Main menu

<img width="367" alt="Screenshot 2023-07-10 at 11 15 40" src="https://github.com/StefanIancu/projects/assets/124818078/1f7e16af-3fb3-496d-a422-2a09fe6cc1fd">

After the user creates an account (or logs with an existing one) they will be prompted into the main menu. 

Here is the basic front panel of the app. They can book a flight, see their reservations and so on. Each choice should be pretty self-explanatory. 

### Booking a flight 

## ->Name

<img width="367" alt="Screenshot 2023-07-10 at 11 16 05" src="https://github.com/StefanIancu/projects/assets/124818078/388b6ebb-4f5e-4658-8069-0ef5256439ab">

Once the user decides to book a flight, they will be asked for their name. This field won't let the user advance unless they type a string. Symbols, spaces, numbers, empty fields won't be allowed. Lower/upper case proof. 

## ->Destination

<img width="288" alt="Screenshot 2023-07-10 at 11 16 15" src="https://github.com/StefanIancu/projects/assets/124818078/c106508c-28e8-401e-8a82-a7d116dd8ad5">

Then the program reads from a csv file the destinations and their starting prices. Basically is showing a brochure of their destinations. 

The user needs to choose a destination from the list. Any other input won't be allowed. 

## ->Flight

<img width="651" alt="Screenshot 2023-07-10 at 11 16 30" src="https://github.com/StefanIancu/projects/assets/124818078/02905d64-ed6a-4438-bf55-91e685bd78c5">

For default each destination has three flights each day. Morning, noon and evening. The user is free to choose from these three options. Any other option won't be allowed. 

*there could be as many flights as the owner decides. 

## ->Extras

<img width="444" alt="Screenshot 2023-07-10 at 11 16 56" src="https://github.com/StefanIancu/projects/assets/124818078/985ae8c9-db35-4dc3-b04b-ae01d6dd31af">

Each user has the option to reserve a particular seat or bring a luggage on board. Answering yes will increase the initial price of the flight. 

Regarding the date, the user can only choose a flight from the future. This option is actually taking the user's input and is comparing with the actual time. So there's no chance for a user to pick a flight from the past. 

The pdf will be generated to the "tickets" folder seen above, going straight to the specified destination folder with the specific flight. They can choose to receive the boarding pass on e-mail as well. Let's say we do. 

Each successfull reservation would directly influence the "available seats" number.

## ->E-mail

<img width="821" alt="Screenshot 2023-07-10 at 11 17 25" src="https://github.com/StefanIancu/projects/assets/124818078/a0e61cbf-2576-42ff-9c29-cd26b4436a60">

The html body of the e-mail is going to adapt and insert for each user the data he chose earlier. There will be a reservation summary along with useful information regarding the flight. The boarding pass will be attached below. Each boarding pass has a an unique combination of a random digit and the actual counter of the tickets. 

## ->Boarding pass

<img width="552" alt="Screenshot 2023-07-10 at 11 17 42" src="https://github.com/StefanIancu/projects/assets/124818078/c044ec18-d0a5-4494-8f4a-5a692400d184">

The generated boarding pass contains essential information as the user's name, their ticket and seat number. Also, there's important information regarding their flight (number, gate, date, time, from, to). 

### See reservations 

<img width="754" alt="Screenshot 2023-07-10 at 11 18 06" src="https://github.com/StefanIancu/projects/assets/124818078/4a917061-aa45-4c6c-9887-3f3049ffba4c">

After the reservation has been completed, the user can find it in "See your reservations" sub-menu. 

This option reads straight from the database of flights and shows only the reservations made by the user who is currently logged in. 

*the "check" at the end stands for "checked-in". 

### Delete reservations 

<img width="737" alt="Screenshot 2023-07-10 at 11 18 35" src="https://github.com/StefanIancu/projects/assets/124818078/60496a21-e9c9-4272-9690-87624e0a7552">

Let's say the user changed his mind and they would like to delete a reservation. They would go to "Delete a reservation", input a certain ticket number and their reservation would be deleted as well as the pdf generated. 

If a user deletes a reservation, the "available seats" number for that particular flight would be updated. 

### Check-in

A user can only check-in a flight 24h or less before departure time. This option takes the flight time and compares it with the current time.

If the difference is higher than 24h, the check-in would be closed:

<img width="751" alt="Screenshot 2023-07-10 at 11 19 12" src="https://github.com/StefanIancu/projects/assets/124818078/248ebd7a-4f4a-4f19-87c4-4b5ede89ce10">

If the difference is lower than 24h, the check-in is open: 

<img width="773" alt="Screenshot 2023-07-10 at 11 21 05" src="https://github.com/StefanIancu/projects/assets/124818078/26330dd5-b85d-4f4c-99f8-3773bf11d366">

The red mark wil turn into a green check if the check-in is successfully completed:

<img width="747" alt="Screenshot 2023-07-10 at 11 21 16" src="https://github.com/StefanIancu/projects/assets/124818078/93824ea4-b2dc-4029-b492-f99be44e0837">

### Get help

<img width="999" alt="Screenshot 2023-07-10 at 12 26 54" src="https://github.com/StefanIancu/projects/assets/124818078/38adced3-96a1-4b1a-8d05-6c04956fd745">

This is the owner's place of giving information or providing any tips. 

*I've used the EU travel guide for reference. 

### Staff options

<img width="391" alt="Screenshot 2023-07-10 at 11 21 47" src="https://github.com/StefanIancu/projects/assets/124818078/00c3b52b-ecb7-45ec-ba46-63158a41ec70">

After a staff member logs in, they have four options to choose from. Basically each option from above has two options. 

For example, "Flight stats" has "General" and "Particular". "General" would pull from the database general information about the flights, while "Particular" would pull for a specific destination. 

"Ticket stats" works exactly the same. Here's the report for "Ticket stats" -> "General". 

<img width="403" alt="Screenshot 2023-07-10 at 11 21 57" src="https://github.com/StefanIancu/projects/assets/124818078/525a2aec-0116-43c7-8a1b-4aa783cda54f">

### Database

## ->User's safety 

<img width="309" alt="Screenshot 2023-07-10 at 11 25 39" src="https://github.com/StefanIancu/projects/assets/124818078/e54beb29-56e4-4743-b322-2b31b83d9c24">

Each user account would be stored in a database. Each password is hashed in a 20 digit code. When logging in, the codes are compared and not the actual passwords. 

The password would never be showed on screen:

<img width="450" alt="Screenshot 2023-07-10 at 12 34 05" src="https://github.com/StefanIancu/projects/assets/124818078/38bf9939-7fec-47bb-836f-5a791d01670a">

## ->Flights

<img width="284" alt="Screenshot 2023-07-10 at 11 25 58" src="https://github.com/StefanIancu/projects/assets/124818078/fd5d8420-a1d5-4ce7-9671-13353e11e593">

Each flight is stored in a database. The staff can add or remove flights whenever they want without even opening the database. There's a function in the program for this that does the job. 




