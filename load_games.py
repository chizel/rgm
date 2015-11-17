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
# games directory
gdir = os.path.join(wdir, 'games')
main_url = 'http://rugame.mobi/game/'
#categories = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 6920, 7169, 7135]
categories = [3]


def create_directory(path, remove_file=True):
    '''Creates directory. If path is a file and remove_file=True than function will
    remove file and create a directory'''
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except:
            if remove_file:
                path = path.rstrip('/')
                os.remove(path)
                os.mkdir(path)
    return 

 
def load_pages(category):
    # creating category directory
    catdir = os.path.join(pdir, str(category))
    create_directory(catdir)

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


def load_games_ids(category):
    '''load games pages from rugame.mobi'''

    cat_dir = os.path.join(pdir, str(category))

    # get all pages
    pages = os.listdir(cat_dir)

    # file with results
    id_file_path = os.path.join(cat_dir, 'ids.txt')
    id_file = open(id_file_path, 'a')

    for page in pages:
        page_path = os.path.join(cat_dir, page)

        with open(page_path, 'r') as f:
            s = f.read()

        m = re.findall('[^|]<a href="/game/(\d*)/">', s)

        for game_id in m:
            id_file.write(game_id)
            id_file.write(' ')

    id_file.close()
    return


def load_game_file(game_id, game_dir, game_page_path, logfile):
    '''load game file and info from rugame.mobi'''

    with open(game_page_path, 'r') as f:
        page = f.read()

    m = re.findall('<a class="dwn_data" href="/game/(\d*)/2/', page)

    # address is not host but ip
    if not m:
        m = re.findall('http://[\d.]*/(\d*)/', page)
        m = set(m)

    for game_link in m:
        try:
            response = urlopen(main_url + game_link)
        except:
            # write error to log-file
            logfile.write(game_id + ' : ' + main_url + game_link + '\n')
            continue

        # generating game name
        game_name = game_link + '.jar'

        game_file_path = os.path.join(game_dir, game_name)
        cont = response.read()

        if not len(cont):
            # write error to log-file
            logfile.write(game_id + ' : ' + main_url + game_link + '\n')
            continue
        with open(game_file_path, 'wb') as f:
            f.write(cont)
    return


def load_games(category):
    '''load games and info from rugame.mobi'''

    category = str(category)
    # current category games' directory
    cat_games_dir = os.path.join(gdir, category)
    create_directory(cat_games_dir)

    # logfile
    logfile = open(os.path.join(cat_games_dir, 'log.txt'), 'a')

    # get games' ids
    gid_source = os.path.join(pdir, category, 'ids.txt')
    with open(gid_source, 'r') as f: 
        games_id = f.read().split()

    for game_id in games_id:
        game_dir = os.path.join(cat_games_dir, game_id)

        if os.path.exists(game_dir):
            continue

        # create current game directory
        create_directory(game_dir)

        response = urlopen(main_url + game_id)
        game_page_path = os.path.join(game_dir, 'page.html')

        with open(game_page_path, 'wb') as f:
            f.write(response.read())
            load_game_file(game_id, game_dir, game_page_path, logfile)
        print('Loaded game: ' + game_id)
    logfile.close()
    return


def main():
    for cat in categories:
        #load_pages(cat)
        #load_games_ids(cat)
        load_games(cat)
    return


if __name__ == "__main__":
    main()
