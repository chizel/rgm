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
categories = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 6920, 7169, 7135]


def create_folder(path, remove_file=True):
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

def load_games(category):
    '''load games and info from rugame.mobi'''

    gid_source = os.path.join(pdir, str(category), 'ids.txt')

    with open(gid_source, 'r') as f: 
        games_id = f.read().split()

    for game_id in games_id:
        response = urlopen(main_url + game_id)
        print(response.read())
        exit()
    return
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


def main():
    load_games(6920)
    exit()
    for cat in categories:
        load_pages(cat)
        load_games_ids(cat)
    return


if __name__ == "__main__":
    main()
