from bs4 import BeautifulSoup

import requests

base_url = 'https://github.com/'


# Parse request content
def parse_html(text):

    return BeautifulSoup(text, 'html.parser')


# Extract file and directory links
def get_dir_links(soup):

    links = []

    grid = soup.find(attrs={'role': 'grid'})

    rows = grid.find_all(attrs={'role': 'row'})

    for row in rows:

        anchor_tag = row.find('a')

        if not anchor_tag or anchor_tag.has_attr('rel'):
            continue

        href = anchor_tag['href'].replace('/' + repo_url, '')

        links.append(href)

    return [link for link in links if link]


def get_folders(links):

    return [link for link in links if 'tree/master' in link]


def get_files(links):

    return [link for link in links if not 'tree/master' in link]


def get_files_links_recursively(url, links, output):

    folders = get_folders(links)

    files = get_files(links)

    for f in files:
        output.append(f)

    if len(folders) > 0:

        for folder in folders:

            r = requests.get(url + folder)

            soup = parse_html(r.text)

            links = get_dir_links(soup)

            get_files_links_recursively(url, links, output)

    return output


with open('repositories.txt') as repositories:

    lines = repositories.read().splitlines()

    for repo_url in lines:

        output = []

        url = base_url + repo_url

        r = requests.get(url)

        soup = parse_html(r.text)

        links = get_dir_links(soup)

        files = get_files_links_recursively(url, links, output)

        for file_dir in files:

            print(file_dir)
