#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import re
import os.path
from bs4 import BeautifulSoup


# work directory
wdir = os.path.dirname(os.path.realpath(__file__))
# pages directory
pdir = os.path.join(wdir, 'pages')
main_url = 'http://rugame.mobi/game/'
categories = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 6920, 7169, 7135]


def load_pages(category):
    # creating category directory
    catdir = os.path.join(pdir, str(category))

    if not os.path.isdir(catdir):
        os.mkdir(catdir)

    cat_url = main_url + str(category) + '/'
    response = urlopen(cat_url)

    # find how much pages does category have
    first_page = response.read()

    with open(os.path.join(catdir, '1.html'), 'wb') as f:
        f.write(first_page)

    s = BeautifulSoup(first_page)
    res = s.find_all('div', attrs={'class': 'page'})
    s = BeautifulSoup(str(res))
    res = s.find_all('a')
    link = str(res[-2])
    nop = re.search('>(.*)<', link)
    num_of_pages = int(nop.group(1))

    # load all the pages
    for i in range(2, num_of_pages + 1):
        page_path = os.path.join(catdir, str(i) + '.html')
        url = cat_url + str(i) + '/'
        response = urlopen(url)
        with open(page_path, 'wb') as f:
            f.write(response.read())
    return


def load_games_pages(category):
    '''load games pages from rugame.mobi'''

    cat_dir = os.path.join(pdir, category)
    pages = os.listdir(cat_dir)
    for page in pages:
        page_path = os.path.join(cat_dir, page)
        with open(page_path, 'r') as f:
            s = BeautifulSoup(f.read())

    #res = s.find_all('div', attrs={'class': 'play-item'})
    #for song_info in res:
        ## file path
        #url = song_info.find('span', attrs={'class': 'playicn'})
        #filename = './fcm/'

        #try:
            ## add artist's name
            #artist = song_info.find('span', attrs={'class': 'ptxt-artist'})
            #filename += artist.a.contents[0]

            ## add song's name and extention
            #sn = song_info.find('span', attrs={'class': 'ptxt-track'})
            #filename += ' - ' + str(sn.a.b.contents[0][1:-1]) + '.mp3'
        #except:
            #filename += '_' + url.a['href'].split('/')[-1] + '.mp3'
            #print filename

        #if os.path.exists(filename):
            #print 'File "' + filename + '" alredy exists!'
        #else:
            #print 'Loading "' + filename + '"'
            #song = urlopen(url.a['href'])

            #with open(filename, 'w') as f:
                #f.write(song.read())
    return


def main():
    load_games_pages(6920)
    exit()
    for cat in categories:
        #load_pages(cat)
        load_games_pages(cat)
    return


if __name__ == "__main__":
    main()
