## Battery percentage notificator - script

### Overlook 

This is a script that runs as long as the laptop's battery reaches the desired percentage. 
When the percentage reaches the desired value, the script closes and sends an e-mail to the user. 

### Purpose 

Prevents laptops from overheating/overcharging. 

### Use

For this script I used:
<li>pyautogui module to make a function that moves the mouse so the laptop won't go to sleep</li>
<li>smptlib for sending the email to the user</li>
<li>psutil to get os information</li>


I've also converted this in an executable format (can be found in "exec_output" folder) which doesn't require and IDE to run. 

### Run

The script asks for a desired percentage: 

<img width="299" alt="Screenshot 2023-07-10 at 14 33 31" src="https://github.com/StefanIancu/projects/assets/124818078/8113459e-c639-4547-be46-ffb9adadac41">

After the user inputs the percentage, the script starts fetching the battery level:

<img width="334" alt="Screenshot 2023-07-10 at 14 35 02" src="https://github.com/StefanIancu/projects/assets/124818078/84666e67-3218-45ff-ba71-74d6170ff4d6">

*default 15 sec, can be changed anytime. with every fetch, the mouse is moving so the sys won't sleep 

When the percentage reaches the desired level, the e-mail pops:

<img width="549" alt="Screenshot 2023-07-10 at 14 41 44" src="https://github.com/StefanIancu/projects/assets/124818078/0b23a15e-55a5-46b5-9b57-6011f04b183c">

And the script closes.