#! /usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import re
import os.path
from bs4 import BeautifulSoup


# work directory
wdir = os.path.dirname(os.path.realpath(__file__))
# pages directory
pdir = os.path.join(wdir, 'pages')


def load_pages(number_of_pages):
    req_url = 'http://rugame.mobi/game/'
    cat = [range(3, 14)]
    cat.extend([6920, 7169, 7135])

    cat = [6920,]#TEMP

    for i in cat:
        # creating category directory
        catdir = os.path.join(pdir, str(i))

        if not os.path.isdir(catdir):
            os.mkdir(catdir)

        url = req_url + str(i)
        response = urlopen(url)

        # find how much pages does category have
        first_page = response.read()

        with open(os.path.join(catdir, '1.html'), 'w') as f:
            f.write(first_page)

        exit()
        s = BeautifulSoup(first_page)
        res = s.find_all('div', attrs={'class': 'page'})
        s = BeautifulSoup(str(res))
        res = s.find_all('a')
        link = str(res[-2])
        nop = re.search('>(.*)<', link)
        num_of_pages = int(nop.group(1))
    
        # load all the pages
        for j in range(2, num_of_pages + 1):
            #print 'loading page: ', str(j)
            page_name = os.path.join(catdir, str(j) + '.html')
            with open(page_name, 'w') as f:
                f.write(response.read())
    return


#def load_songs(page):
    #'''load songs from free music archive'''

    #with open('./pages/Free Music Archive: Classical' + str(page), 'r') as f:
        #s = BeautifulSoup(f.read())

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
    #return


def main():
    load_pages(140)
    exit()

    start = 5

    for i in range(start, start + 1):
        load_songs(i)
    return


if __name__ == "__main__":
    main()
