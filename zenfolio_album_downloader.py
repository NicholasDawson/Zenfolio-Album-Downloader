from bs4 import BeautifulSoup
from os import getcwd, makedirs
from os.path import isdir
import requests

def createdir(path):
    if not isdir(path):
        makedirs(path)

def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")

def download_file(url, path):
    filename = path + '/' + url[url.rfind('/') + 1:]
    with open(filename, 'wb') as file:
        r = requests.get(url)
        file.write(r.content)
    print('{} downloaded as {}'.format(url, filename))
    return r.status_code

def download_zenfolio_img(url, folder):
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    image = soup.find('meta', {'property': "og:image"})['content'].replace('4.jpg', '5.jpg')
    download_file(image, getcwd() + '/' + folder)
    try:
        next = soup.find('a', {'class': "button photoLtRtTh-navigationButton photoLtRtTh-navigationNext invisible"})['href']
    except TypeError:
        return False
    return next

def download_zenfolio_album(url):
    URL_BASE = '/'.join(url.split('/')[:3])

    print('Fetching album metadata...')
    album_soup = BeautifulSoup(requests.get(url).content, 'lxml')
    first_image = album_soup.find('a', {'class': 'pv-inner'})['href']
    album_title = make_safe_filename(album_soup.find('span', {'class': 'title breadcrumbs-font3'}).text)

    print('Creating directory...')
    createdir(album_title)

    print('Downloading images...')
    next = download_zenfolio_img(URL_BASE + first_image, album_title)
    while next:
        next = download_zenfolio_img(URL_BASE + next, album_title)

# =====================================================
print('Zenfolio album downloader\nBy: Nicholas Dawson')
print('=' * 20)
album_url = input('Enter the album url: ')
download_zenfolio_album(album_url)
