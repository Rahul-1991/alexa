import requests


class GithubAPI:

    def __init__(self):
        pass

    @staticmethod
    def get_best_repos(lang):
        response = requests.get('https://api.github.com/search/repositories?q=stars:%3E1+language:{}&sort=stars&order=desc&type=Repositories'.format(lang))
        if response.status_code == 200:
            items = response.json().get('items', [])
            return map(lambda info: info.get('name'), items)[:5]
        else:
            return []
