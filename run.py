from bs4 import BeautifulSoup

import requests

base_url = 'https://github.com/'

with open('repositories.txt') as repositories:

    lines = repositories.read().splitlines()

    for repo_url in lines:

        url = base_url + repo_url

        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')

        print(soup.title)