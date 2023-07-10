import psutil
import time
import pyautogui
import random
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#set email credentials
EMAIL_PASS = "fshbrcqyywpavsbd"
EMAIL_USER = "pythontest.odyssey2001@gmail.com"
EMAIL_SERVER = "smtp.gmail.com"
EMAIL_SERVER_PORT = 465 # post smtp pentru conexiuni securizate

#send email to user
def send_battery_email(user_email, user_name, battery):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Battery fully charged"
    message["From"] = EMAIL_USER
    message["To"] = user_email

    html = f"""
    <html>
    <body>
        <h2>Hello {user_name}! Your battery is fully charged!</h2>
        <p>Battery info: {battery[0]}</p>
        <p>This email is sent from a <b>Python</b> script.</p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    #setting a server
    server = smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_SERVER_PORT)
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(
        EMAIL_USER,
        user_email,
        message.as_string()
    )

#return true if percentage == custom value
def get_battery_percentage(value: int):
    battery = psutil.sensors_battery()
    if battery[0] == value:
        return True
    
#stop the screen go AFK
def move_mouse():
    x = random.randint(600, 800)
    y = random.randint(200, 600)
    pyautogui.moveTo(x, y, 0.5)
       

battery = psutil.sensors_battery()

#loop while os is checking percentage and mouse is moving to stop AFK.
#when percentage == value loop breaks and sends email to user
percentage = int(input("What percentage interests you? ")) 
print(f"Got it. Will let you know when battery is {percentage}%.")
while True: 
        time.sleep(15)
        move_mouse()
        print(f"Fetching battery info...{battery[0]}%")   
        if get_battery_percentage(percentage):
            send_battery_email("iancustefan28@yahoo.com", "Stefan Iancu", battery)
            break

