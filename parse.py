#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import re
import os.path
import shutil
from bs4 import BeautifulSoup


# work directory
wdir = os.path.dirname(os.path.realpath(__file__))
# games directory
gdir = os.path.join(wdir, 'games/')
#categories = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 6920, 7169, 7135]
categories = [6920]


def parse_games(category):
    '''rename games files to readable names'''
    category = str(category)
    # current category games' directory
    cat_games_dir = os.path.join(gdir, category)

    games_ids = os.listdir(cat_games_dir)

    for game_id in games_ids:
        game_dir = os.path.join(cat_games_dir, game_id)

        if len(os.listdir(game_dir)) < 2:
            continue

        game_page_path = os.path.join(game_dir, 'page.html')

        with open(game_page_path, 'r') as f:
            page = f.read()

        game_name = re.search('<title>(.*) скачать бесплатно на телефон</title>', page)
        game_name = game_name.group(1)
        m = re.findall('<font color="#"><hr/></font>([\S\s]*?)<br/><a class="dwn_data" href="/game/(\d*)/', page)

        for l in m:
            game_file = os.path.join(game_dir, l[1] + '.jar')

            if os.path.exists(game_file):
                tmp = l[0].replace(',', '_')
                tmp = tmp.replace('/', '_')
                old_name = tmp.split()

                if len(old_name) < 4:
                    new_name = old_name[0] + '_' + old_name[2]
                else:
                    new_name = old_name[0] + '_' + old_name[2] + old_name[3]

                    if len(new_name) > 20:
                        new_name = new_name[:20]

                    new_name = new_name + '_' + old_name[-1] + '.jar'
                    new_name_path = os.path.join(game_dir, new_name)

                # write game_id to directory for future use
                with open(os.path.join(game_dir, game_id), 'w') as f:
                    f.write('')

                # rename gamefile
                os.rename(game_file, new_name_path)
            else:
                print(game_name, game_file)
        # rename gamedirectory from id to normal name
        new_game_dir = os.path.join(cat_games_dir, game_name)
        shutil.move(game_dir, new_game_dir)
    return


def main():
    for cat in categories:
        parse_games(cat)
    return


if __name__ == "__main__":
    main()
