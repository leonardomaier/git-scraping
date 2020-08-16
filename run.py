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


def convert_kb_to_bytes(kb):
    return float(kb) * 1000


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

            file_info = filename.split('.')

            file_ext = file_info[len(file_info) - 1]

            file_data_div = soup.select('div.Box-header.py-2 .text-mono')

            file_data_arr = file_data_div[0].text.strip().split(' ')

            print(filename)

            if file_ext not in extension_data:

                total_bytes = float(file_data_arr[13])

                if file_data_arr[14] == 'KB':
                    total_bytes = convert_kb_to_bytes(total_bytes)

                extension_data[file_ext] = {
                    'total_lines': int(file_data_arr[0]),
                    'total_bytes': total_bytes
                }

            else:

                extension_data[file_ext]['total_lines'] += int(
                    file_data_arr[0])

                if file_data_arr[14] == 'KB':
                    extension_data[file_ext]['total_bytes'] += convert_kb_to_bytes(
                        file_data_arr[13])
                else:
                    extension_data[file_ext]['total_bytes'] += float(
                        file_data_arr[13])

        for ext in extension_data:

            output_file.write('--> ' + ext + '\n\n')
            
            output_file.write('Total bytes: ' + str(extension_data[ext]['total_bytes']) + '\n')
            output_file.write('Total lines: ' +
                              str(extension_data[ext]['total_lines']) + '\n\n')
