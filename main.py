##################### Extra Hard Starting Project ######################
import random
import datetime as dt
import smtplib
import pandas
import os

HOST = 'smtp.gmail.com'
PORT = 587
APP_PW = os.environ.get("MY_PASSWORD")
MY_EMAIL = os.environ.get("MY_EMAIL")
# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv
birthday_dataframe = pandas.read_csv('birthdays.csv')
birthday_month = birthday_dataframe.month.to_list()
birthday_day = birthday_dataframe.day.to_list()

def check_birthday():
    now = dt.datetime.now()
    today = (now.month, now.day)

    actual_birthdays = []
    for i in range(len(birthday_month)):
        actual_birthdays.append((birthday_month[i], birthday_day[i]))

    if today in actual_birthdays:
        return today
    return False

def set_message(birthday):
    letters_list = ['./letter_templates/letter_1.txt', './letter_templates/letter_2.txt', './letter_templates/letter_3.txt']
    template_path = random.choice(letters_list)
    month = birthday[0]
    day = birthday[1]
    message = ""
    with open(template_path, 'r') as letter:
        message = letter.read()

    birth_day_row = birthday_dataframe[(birthday_dataframe.month == month) & (birthday_dataframe.day == day)]
    name = birth_day_row.name.item()
    email = birth_day_row.email.item()

    message = message.replace("[NAME]", name)
    return message, email


def send_mail(message_to_send, email_to_send_to):
    with smtplib.SMTP(host=HOST, port=PORT) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=APP_PW)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=email_to_send_to, msg=f'Subject: Happy Birthday!\n\n{message_to_send}')


user_birthday = check_birthday()
if user_birthday:
    message, email = set_message(user_birthday)
    send_mail(message, email)




