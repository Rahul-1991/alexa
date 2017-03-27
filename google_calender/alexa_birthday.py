from flask import Flask
from flask_ask import Ask, statement, question, session
from google_calender_api import GoogleCalenderWrapper
from datetime import datetime
import re

app = Flask(__name__)
ask = Ask(app, "/")


@ask.launch
def birthday_app():
    return question('Retrieving events from the calender..... Events retrieved')


def get_current_date():
    return datetime.now().date()


def is_event_today(event):
    event_date = event.get('date')
    event_date_object = datetime.strptime(event_date, '%d %B %Y').date()
    today_date_object = get_current_date()
    return event_date_object == today_date_object


def birthday_today_list(calender_info):
    event_list = list()
    for event in calender_info:
        if is_event_today(event):
            event_list.append(re.sub("\'s birthday", '', event.get('event')))
    return event_list


@ask.intent("BirthdayIntent")
def retrieve_today_birthday():
    calender_info = GoogleCalenderWrapper().get_event_summary()
    today_birthday_list = birthday_today_list(calender_info)
    birthday_speech = 'Sir i have found the following people who have birthday today. '
    for event in today_birthday_list:
        birthday_speech += event + '. '
    return statement(birthday_speech)

if __name__ == '__main__':
    app.run(debug=True)