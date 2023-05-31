from sqlite3 import Cursor
import psycopg2
import pandas as pd
import csv
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import datetime
import pytz

 

#establishing the connection
conn = psycopg2.connect(
   database="mydb", user='postgres', password='123456', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

cursor = conn.cursor()
#Preparing query to create a database
# sql = '''CREATE database IF NOT EXISTS mydb''';
# #Creating a database
# cursor.execute(sql)
# print("Database created successfully")



#Creating a cursor object using the cursor() method
# cursor = conn.cursor()


 


# cursor.execute("CREATE TABLE IF NOT EXISTS employee(Name VARCHAR(40),designation VARCHAR(100), salary INT)")
# print("Table created successfully")
# cursor.execute("INSERT INTO employee Values('Saifur Rahman','Data Analyst',20000)")
# cursor.execute("INSERT INTO employee Values('Rahul Paul','AI',30000)")
# print("Data Inserted Successfully")


# # cursor.execute("CREATE TABLE IF NOT EXISTS country(id SERIAL,province_state VARCHAR(100), country_region VARCHAR(100),lat VARCHAR(11),lon VARCHAR(11),date VARCHAR(40),confirmed INT,deats INT)")
# # print("Country Table created successfully")
cursor.execute(
    """CREATE TABLE IF NOT EXISTS corona(
    id SERIAL NOT NULL PRIMARY KEY,
    province_state VARCHAR(100),
    country VARCHAR(10),
    lat FLOAT,
    lon FLOAT,
    date DATE,
    confirmed INT,
    deaths INT
     )
    """)
# with open("usa_county_wise.csv","r") as f:
#     reader = csv.reader(f)
#     next(reader)
#     for row in reader:
#         cursor.execute(
#             "INSERT INTO corona VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
#             row
#         )
print("Data Inserted in corona Table Successfully")
show_all_data = cursor.execute("SELECT * FROM corona")
one = cursor.fetchone()
all = cursor.fetchall()
print(all[-1])
#print(all)
print(type(one))
data = pd.DataFrame(all)
x = data[6]
y = data[7]
fig = plt.figure()
plt.hist(x, bins =5)
plt.show()
fig.savefig("histogram.png")


tz_NY = pytz.timezone('Asia/Dhaka')
# # Email configuration
sender_email = 'junayed.ndc16@gmail.com'
sender_password = 'vyoyranzxxebvonv'
receiver_email = 'almehady@gmail.com'
# bcc_email = 'rsaifurrahman175@gmail.com'
date = datetime.datetime.now(tz_NY)
subject = "Histogram Report "+date.strftime("%d")+" "+date.strftime("%B"+", "+date.strftime("%Y"))
message = " Dear Sir, \n\n  This is my report \n\n MD Junayed Hossain \n Data Analyst\n"+" "+date.strftime("%c")
# # Create the email message


msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
# msg['Bcc'] = bcc_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

# Attach the histogram.png file

with open('histogram.png', 'rb') as file:
    image = MIMEImage(file.read(), name='histogram.png')
    msg.attach(image)

# Connect to the SMTP server and send the email


with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
print('Email sent successfully!')
#Closing the connection
conn.close()