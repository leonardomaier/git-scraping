from bs4 import BeautifulSoup

import requests

base_url = 'https://github.com/'


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

            soup = request_and_parse(url + folder)

            links = get_dir_links(soup)

            get_files_links_recursively(url, links, output)

    return output


def request_and_parse(url):

    response = requests.get(url)

    return BeautifulSoup(response.text, 'html.parser')


with open('repositories.txt') as repositories:

    lines = repositories.read().splitlines()

    for repo_url in lines:

        print('-------------- ' + repo_url + ' --------------')

        output_file = open(
            'outputs/' + repo_url.replace('/', '_') + '.txt', 'w')

        output = []

        url = base_url + repo_url

        soup = request_and_parse(url)

        links = get_dir_links(soup)

        files = get_files_links_recursively(url, links, output)

        extension_data = {}

        for file_dir in files:

            soup = request_and_parse(url + file_dir)

            filename = soup.find('strong', class_='final-path').text

            file_ext = filename.split('.')[1]

            file_data_div = soup.select('div.Box-header.py-2 .text-mono')

            file_data_arr = file_data_div[0].text.strip().split(' ')

            print(filename)

            if file_ext not in extension_data:

                extension_data[file_ext] = {
                    'total_lines': int(file_data_arr[0])
                }

            else:

                extension_data[file_ext]['total_lines'] += int(file_data_arr[0])

        output_file.write('Extensão   |   Linhas   |   Bytes\n')

        for ext in extension_data:

            output_file.write(ext + '    | ' + str(extension_data[ext]['total_lines']) + '   |\n')
