import smtplib, ssl
import os
import mysql.connector
from email.message import EmailMessage

from email.mime.text import MIMEText

# user system variable with email and password to protect the user from security breach.
email_bot_variable = os.environ.get('email_bot')
email_bot_pass_variable = os.environ.get('email_bot_pass')

# using a variable to store the receiver email, therefore I can iterate from list of subscribers.

mydb_subscribers = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb"
)

db_to_py = mydb_subscribers.cursor()
db_to_py.execute("SELECT email FROM email_table")
myresult = db_to_py.fetchall()
result = [list(i) for i in myresult]
final_result = [item for sublist in result for item in sublist]
receiver_email = final_result

# the code below is directly taken from the youtube tutorial I used to guide through the smtplib library.

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: # email server ssl = Secure Sockets Layer
    smtp.login(email_bot_variable, email_bot_pass_variable)
    # initially used port 587 and then change to port 465
    # for encrypting the communication over the internet
    # i have left the previous code in case the new implementation
    # stops working properly

    msg = EmailMessage()
    msg['Subject'] = 'newsletter test'
    msg['From'] = email_bot_variable
    msg['to'] = receiver_email
    msg.set_content('plain text email, test test test test test\nsent from python')
    html_newsletter = open('beefree-3h533ukhaie.html').read()
    msg.add_alternative(html_newsletter, subtype='html')
    smtp.send_message(msg)

nl = '\n'
print(f"Email sent to:{nl}{nl.join(final_result)}")
print('All newsletters sent successfully!')
