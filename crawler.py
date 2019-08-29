# Web Crawler
# By Judah Goff

from urllib.request import urlopen, Request
from sys import argv, maxsize
from hashlib import md5
from os import path, mkdir
from time import sleep
from bs4 import BeautifulSoup


class Settings:
    def __init__(self, pages_to_download, pause_length, recursive_mode, domain_name):
        self.pages_to_download = pages_to_download
        self.pause_length = pause_length
        self.recursive_mode = recursive_mode
        self.domain_name = domain_name


def set_arguments():
    if len(argv) > 0:
        # Remove the file name
        del argv[0]
        if len(argv) == 0:
            print("Error: Supply a URL to retrieve")
            return
    recursive_mode = False
    pause_length = 2
    # Max size of an int https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints
    pages_to_download = maxsize

    arguments = argv[:-1]
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument == '-h':
            print('HU-Crawls: Created by Judah Goff. Possible arguments include:\n\t' +
                  '-n *total*   - Specify the total number of pages to download. Once the' +
                  ' crawler has downloaded the *total* number of pages or the frontier' +
                  ' is empty, the crawler should terminate.\n\t' +
                  '-r           - Turn on recursive retrieving, which follows links in discovered' +
                  'web pages. Without -r, only the given URL is downloaded, then the ' +
                  'crawler terminates.\n\t' +
                  '-w *seconds* - Wait the given number of seconds between HTTP requests.' +
                  ' If no -w option is specified, the default wait should be 2 seconds.\n\t' +
                  '-h           - Shows this help page.')
        recursive_mode = '-r' in arguments
        if argument == '-n' and index + 1 < len(arguments):
            try:
                pages_to_download = int(arguments[index + 1])
                index += 1
            except ValueError:
                print('Error: Number of pages must be a number.')
                return
        if argument == '-w' and index + 1 < len(arguments):
            try:
                pause_length = int(arguments[index + 1])
                index += 1
            except ValueError:
                print('Error: Duration of pause must be a number.')
                return

        index += 1
    return pages_to_download, pause_length, recursive_mode, argv[len(argv) - 1]


def find_domain_name(url):
    # Gets harding from http://cs.harding.edu/
    # url_without_http = url[url.find('//') + 2:]
    # domain_and_rest = url_without_http[url_without_http.find('.') + 1:]
    # return domain_and_rest[:domain_and_rest.find('.')]

    # Gets cs.harding from http://cs.harding.edu/
    url_without_http = url[url.find('//') + 2:]
    domain_and_rest = url_without_http[:url_without_http.find('.', url_without_http.find('.') + 1)]
    # return domain_and_rest[:domain_and_rest.find('.')]
    return domain_and_rest


def start_crawler():
    pages_to_download, pause_length, recursive_mode, url = set_arguments()

    # Create target Directory if don't exist https://thispointer.com/how-to-create-a-directory-in-python/
    if not path.exists('pages'):
        mkdir('pages')

    domain_name = find_domain_name(url)
    print('domain', domain_name)
    settings = Settings(pages_to_download, pause_length, recursive_mode, domain_name)
    crawl(url, settings, 0, [], [])
    print('Finished crawling!')


def save_to_file(response, html, settings):
    filename = 'pages/' + md5(response.geturl().encode()).hexdigest() + '.html'
    with open(filename, 'w') as file_writer:
        file_writer.write(response.geturl() + '\n' + str(response.info()) + html)
        print('-- Saved to ' + filename)
        # Pause program https://www.pythoncentral.io/pythons-time-sleep-pause-wait-sleep-stop-your-code/
        sleep(settings.pause_length)


def crawl(url, settings, pages_downloaded, frontier, visited):
    if settings.pages_to_download > pages_downloaded:
        response = urlopen(Request(url, headers={'User-Agent': 'WebSci Crawler'}))
        print('Crawling: ' + response.geturl())
        # How to get MIME type https://stackoverflow.com/questions/12474406/python-how-to-get-the-content-type-of-an-url
        mime_type = response.info().get_content_type()
        if mime_type == 'text/html':
            html = response.read()
            html = str(html, encoding='utf-8')
            soup = BeautifulSoup(html, features="html.parser")
            links = soup('a')
            for link in links:
                print(link.get('href'))

            save_to_file(response, html, settings)
        else:
            print('-- Skipping ' + response.info().get_content_type())
    else:
        print('Limit ' + settings.pages_to_download + ' reached.')


start_crawler()
