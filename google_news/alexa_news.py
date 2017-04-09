from flask import Flask
from flask_ask import Ask, statement, question, session
from google_news_api import GoogleNews

app = Flask(__name__)
ask = Ask(app, "/")


@ask.launch
def new_game():
    session.attributes['last_intent'] = 'Launch'
    return question('You can get the top 5 news for any place. Which place will it be ?')


@ask.intent('NewsIntent', mapping={'place': 'place'})
def news_app(place):
    try:
        news_title_list = GoogleNews().main(place)
    except Exception as e:
        news_title_list = []

    if not news_title_list:
        return statement('Sorry. Could not find any news for %s' % place)
    speech = ''
    for title in news_title_list:
        title, source = title.rsplit('-', 1)
        speech += 'According to %s %s.' % (source, title)
    return statement(speech)


@ask.intent('AMAZON.HelpIntent')
def get_help():
    if session.attributes.get('last_intent') == 'Launch':
        return question('I can provide you with the top 5 news for any place you ask me about. '
                        'Just tell me the name of the place and i will read the news to you. '
                        'So which place do you want to know about ?')


@ask.intent('AMAZON.CancelIntent')
def cancel_request():
    return statement('Thank you for using the app. Have a good day')


@ask.intent('AMAZON.StopIntent')
def stop_app():
    return statement('Thank you for using the app. Have a good day')


if __name__ == '__main__':
    app.run(debug=True)
