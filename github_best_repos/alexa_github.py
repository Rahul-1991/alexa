from flask import Flask
from flask_ask import Ask, statement, question, session
from github_api import GithubAPI

app = Flask(__name__)
ask = Ask(app, "/")


@ask.launch
def introduction():
    session.attributes['last_intent'] = 'Launch'
    return question('You can get the top 5 repos for a computer language. Which language will it be ?')


@ask.intent('RepoListIntent', mapping={'language': 'language'})
def github_app(language):
    try:
        repo_list = GithubAPI().get_best_repos(language)
    except Exception as e:
        repo_list = []

    if not repo_list:
        return statement('Sorry. Could not find any repos for %s' % language)
    speech = 'I found the following repos with the highest ratings. '
    for repo in repo_list:
        speech += repo + ','
    return statement(speech)


@ask.intent('AMAZON.HelpIntent')
def get_help():
    if session.attributes.get('last_intent') == 'Launch':
        return question('I can provide you with the top 5 repositories of github for any language you ask me about. '
                        'Just tell me the language and i will list the repo names for you. '
                        'So which language do you want to know about ?')


@ask.intent('AMAZON.CancelIntent')
def cancel_request():
    return statement('Thank you for using the app. Have a good day')


@ask.intent('AMAZON.StopIntent')
def stop_app():
    return statement('Thank you for using the app. Have a good day')


if __name__ == '__main__':
    app.run(debug=True)
