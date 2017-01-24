#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os.path
import sqlite3
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup


class LoadGames():
    # working directory
    wdir = os.path.dirname(os.path.realpath(__file__))
    main_url = 'http://rugame.mobi/game/'
    # categories id
    categories = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 6920, 7169, 7135]

    def __init__(self, files_dir, db_name='dbgames.db'):
        # directory with pages of list of games
        self.pdir = os.path.join(files_dir, 'pages')
        # directory with game files
        self.gdir = os.path.join(files_dir, 'games')
        self.db_name = db_name

    def create_directory(self, path, remove_file=True):
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

    def load_pages(self, category):
        '''loads pages with list of games links'''
        # connecting to db
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        # creating category directory
        catdir = os.path.join(self.pdir, str(category))
        self.create_directory(catdir)

        # category url
        cat_url = self.main_url + str(category) + '/'
        response = urlopen(cat_url)

        # find how much pages does category have
        first_page = response.read()
        s = BeautifulSoup(first_page)
        res = s.find_all('div', attrs={'class': 'page'})
        s = BeautifulSoup(str(res))
        links = s.find_all('a')
        link = str(links[-2])
        r = re.search('>(.*)<', link)
        num_of_pages = int(r.group(1))

        # load all the pages
        for i in range(1, num_of_pages + 1):
            page_path = os.path.join(catdir, str(i) + '.html')
            url = cat_url + str(i) + '/'
            print('Loading: ', url)
            response = urlopen(url)
            content = response.read()
            content = content.decode('utf8')
            result = self.load_games_ids(category, content)
            # no new games on the page, nothing to load more
            if not result:
                break
            #with open(page_path, 'wb') as f:
            #    f.write(response.read())
        self.conn.close()

    def check_games(self, page):
        m = re.findall('[^|]<a href="/game/(\d*)/">', page)
        games_ids = []

        for game_id in m:
            # checking is game already in the db
            self.cursor.execute(
                'SELECT COUNT(*) FROM games WHERE id=?',
                (game_id,))
            if self.cursor.fetchone()[0]:
                print('skip: ', game_id)
                continue
            games_ids.append(game_id)
        return games_ids

    def load_games_ids(self, category, page=False):
        '''loads games ids'''
        cat_dir = os.path.join(self.pdir, str(category))

        if page:
            game_ids = self.check_games(page)
        else:
            # get all pages
            pages = os.listdir(cat_dir)

            for page_id in pages:
                page_path = os.path.join(cat_dir, page_id)

                with open(page_path, 'r') as f:
                    s = f.read()
                tmp_game_ids = self.check_games(s)
                if not tmp_game_ids:
                    break
                game_ids.extend(tmp_game_ids)

        if not game_ids:
            return False

        # write games' ids to the file
        id_file_path = os.path.join(cat_dir, 'ids.txt')
        id_file = open(id_file_path, 'a')
        id_file.write(' '.join(game_ids))
        id_file.write(' ')
        id_file.close()
        return True

    def load_game_file(self, game_id, game_dir, game_page_path, logfile):
        '''load game files and game info'''

        with open(game_page_path, 'r') as f:
            page = f.read()

        m = re.findall('<a class="dwn_data" href="/game/(\d*)/2/', page)

        # if address is not host but ip
        if not m:
            m = re.findall('http://[\d.]*/(\d*)/', page)
            m = set(m)

        for game_link in m:
            req = urllib.request.Request(self.main_url + game_link)
            req.add_header(
                'user-agent',
                '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36
                (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'''
                )

            try:
                response = urllib.request.urlopen(req)
            except:
                # write error to log-file
                logfile.write(game_id + ' : ' + self.main_url + game_link + '\n')
                continue

            # generating game name
            game_name = game_link + '.jar'

            game_file_path = os.path.join(game_dir, game_name)
            cont = response.read()

            if not len(cont):
                # write error to log-file
                logfile.write(game_id + ' : ' + self.main_url + game_link + '\n')
                continue
            with open(game_file_path, 'wb') as f:
                f.write(cont)


    def load_games(self, category):
        '''load games and info from rugame.mobi'''

        category = str(category)
        # current category games' directory
        cat_games_dir = os.path.join(self, self.gdir, category)
        self.create_directory(cat_games_dir)

        # logfile
        logfile = open(os.path.join(cat_games_dir, 'log.txt'), 'a')

        # get games' ids
        gid_source = os.path.join(self.pdir, category, 'ids.txt')

        with open(gid_source, 'r') as f: 
            games_id = f.read().split()

        for game_id in games_id:
            game_dir = os.path.join(cat_games_dir, game_id)

            # game already loaded
            if os.path.exists(game_dir):
                continue

            # create current game directory
            self.create_directory(game_dir)

            response = urlopen(self.main_url + game_id)
            game_page_path = os.path.join(game_dir, 'page.html')

            print('Loading game: ' + game_id)
            with open(game_page_path, 'wb') as f:
                f.write(response.read())
                self.load_game_file(game_id, game_dir, game_page_path, logfile)
        logfile.close()


def main():
    files_dir = '/media/ext4files/rgm/'
    lg = LoadGames(files_dir)
    cat = 3
    lg.load_games(cat)
    return
    for cat in lg.categories[1:]:
        #lg.load_pages(cat)
        lg.load_games(cat)


if __name__ == "__main__":
    main()
