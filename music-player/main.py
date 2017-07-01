import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from music_player import MediaPlayer

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():
    return question('What kind of music would you like to play Sir ?')


@ask.intent("PlayerIntent", convert={'mood': 'mood'})
def answer(mood):
        return question('Collected list of songs as per your {} mood. Start playing ?'.format(mood))


@ask.intent("YesIntent")
def play():
    MediaPlayer().play()

if __name__ == '__main__':
    app.run(debug=True)