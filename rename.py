#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os.path
import shutil
import sqlite3
from html.parser import HTMLParser


# working directory
wdir = os.path.dirname(os.path.realpath(__file__))

# directory with game files
gdir = os.path.join(wdir, 'games/')

# games' categories
categories = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 6920, 7169, 7135]


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def parse_games(category):
    '''rename games files to readable names'''

    # connecting to db
    conn = sqlite3.connect('dbgames.db')
    cursor = conn.cursor()

    category = str(category)

    # current category's directory
    cat_games_dir = os.path.join(gdir, category)

    # opening log file
    logf = open(os.path.join(cat_games_dir, 'log.txt'), 'w')

    game_ids = os.listdir(cat_games_dir)

    for game_id in game_ids:
        try:
            int(game_id)
        except:
            # directory's name was renaimed earlier, skip it
            continue

        # checking is game already in the db
        cursor.execute('SELECT COUNT(*) FROM games WHERE id=?', (game_id,))
        if cursor.fetchone()[0]:
            continue

        # directory with current game's files
        game_dir = os.path.join(cat_games_dir, game_id)

        # are there any game file (1 file - game's page)
        if len(os.listdir(game_dir)) < 2:
            logf.write('Empty ' + game_dir + '\n')
            print('Empty', game_dir)
            continue

        game_page_path = os.path.join(game_dir, 'page.html')

        with open(game_page_path, 'r') as f:
            page = f.read()

        game_name = re.search(
            '<title>(.*) скачать бесплатно на телефон</title>',
            page)
        game_name = game_name.group(1)
        game_name = game_name.replace('/', '-')

        # extracting game info
        m = re.search('\d+</a> <br/><br/>(.*)<b>Загрузил', page, re.DOTALL)
        game_info = ''

        if m:
            game_info = strip_tags(m.group(1))
            game_info = game_info.strip()

        # CREATE TABLE game (id INT PRIMARY KEY UNIQUE, name CHAR, category INT, info CHAR);
        cursor.execute(
            'INSERT INTO games (id, name, category, info) VALUES (?,?,?,?)',
            (game_id, game_name, category, game_info))

        # game's files
        links = re.findall(
            'hr/></font>([\S\s]*?)<br/><a class="dwn_data" href="/game/(\d*)/',
            page)

        for link in links:
            game_file = os.path.join(game_dir, link[1] + '.jar')

            # is game info standard
            if not os.path.exists(game_file):
                logf.write('Game info: ' + game_name + ' ' + game_file + '\n')
                print('Game info isn\'t standart', game_name, game_file)
                continue

            gamefile_specifications = link[0].strip()
            #new_name = game_name[:25]
            new_name = game_name
            screen = ''
            lang = ''

            # screen resolution
            tmp = re.search('^\d{3}x\d{3}', gamefile_specifications,
                            re.IGNORECASE)
            if tmp:
                screen = tmp.group(0)
                new_name += '_' + screen
                width = screen[:3]
                height = screen[-3:]
            else:
                width = 0
                height = 0

            # game language (eng/ru)
            tmp = re.search('ENG|RUS|EN|RU', gamefile_specifications,
                            re.IGNORECASE)

            if tmp:
                lang = tmp.group(0)
                new_name += '_' + lang


            new_name += '_' + game_id
            new_name += '.jar'
            new_name_path = os.path.join(game_dir, new_name)

            # checking is file with this name already exists
            i = 0
            tmp = new_name_path[:]

            while os.path.exists(tmp):
                # file name without '.jar'
                tmp = new_name_path[:-4]
                tmp += '_' 
                tmp += str(i)
                tmp += '.jar'
                i += 1

            new_name_path = tmp

#CREATE TABLE game_files (game_id INT, width INT, height INT, oldname CHAR, filename CHAR, FOREIGN KEY(game_id) REFERENCES games(id));
            # writing to db
            cursor.execute(
                '''INSERT INTO game_files (game_id, width, height, oldname,
                filename) VALUES (?,?,?,?,?)''',
                (game_id, height, width, link[1], new_name))

            # write game_id to directory for future use
            #with open(os.path.join(game_dir, game_id), 'w') as f:
                #f.write('')

            # rename gamefile
            os.rename(game_file, new_name_path)

        conn.commit()

        # rename gamedirectory from id to normal name
        new_game_dir = os.path.join(cat_games_dir, game_name)
        shutil.move(game_dir, new_game_dir)
    conn.close()


def main():
    for cat in categories:
        parse_games(cat)


if __name__ == "__main__":
    main()
