from flask import Flask
from flask_ask import Ask, statement, question, session
from ola_utility import OlaUtility

app = Flask(__name__)
ask = Ask(app, "/")


ola_handle = OlaUtility()

@ask.launch
def new_game():
    session.attributes['last_intent'] = 'Launch'
    session.attributes['ask_for_booking'] = True
    return question('Would you like to book a cab Sir ?')


def check_for_cab():
    ride_info = ola_handle.get_cabs_details()
    alexa_statement = 'Looking for your ride to office. '
    if ride_info:
        alexa_statement += 'A share ride is {} mins away and will cost you {}. Would you like to book it ?'.format(
            ride_info.get('eta'), ride_info.get('price')
        )
    else:
        alexa_statement += 'No cabs are going in your direction sir'
    session.attributes['book_cab'] = True
    return alexa_statement


def book_cab():
    booked_cab_details = ola_handle.book_cab()
    alexa_statement = "Booking a cab for you. "
    if booked_cab_details:
        alexa_statement += 'A {} {} with car number {} is on the way and will reach in {} mins. ' \
                           'Your OTP is {}. Have a safe journey sir. Bye'.format(
                                    booked_cab_details.get('car_color'),
                                    booked_cab_details.get('car_model'),
                                    booked_cab_details.get('cab_number'),
                                    booked_cab_details.get('eta'),
                                    booked_cab_details.get('otp')
                                )
    else:
        alexa_statement += 'No cabs are going in your direction sir'
    return alexa_statement


@ask.intent('YesIntent')
def accept_book_prompt():
    alexa_statement = ''
    if session.attributes['ask_for_booking']:
        session.attributes['ask_for_booking'] = False
        alexa_statement = check_for_cab()
    elif session.attributes['book_cab']:
        session.attributes['book_cab'] = False
        alexa_statement = book_cab()
    return question(alexa_statement)


@ask.intent('AMAZON.HelpIntent')
def get_help():
    if session.attributes.get('last_intent') == 'Launch':
        return question('I can book a cab for you. Would you like to book ?')


@ask.intent('AMAZON.CancelIntent')
def cancel_request():
    return statement('Thank you for using the app. Have a good day')


@ask.intent('AMAZON.StopIntent')
def stop_app():
    return statement('Thank you for using the app. Have a good day')


if __name__ == '__main__':
    app.run(debug=True)
