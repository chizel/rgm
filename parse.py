#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import re
import os.path
import shutil
from bs4 import BeautifulSoup
from html.parser import HTMLParser


# working directory
wdir = os.path.dirname(os.path.realpath(__file__))

# directory with game files
gdir = os.path.join(wdir, 'games/')

# games' categories
#categories = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 6920, 7169, 7135]
categories = [5]


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

    category = str(category)

    # current category directory
    cat_games_dir = os.path.join(gdir, category)

    game_ids = os.listdir(cat_games_dir)

    for game_id in game_ids:
        try:
            int(game_id)
        except:
            # directory's name was renaimed earlier, nothing to do
            continue

        # directory with current game's files
        game_dir = os.path.join(cat_games_dir, game_id)

        # are there any game file (1 file - game's page)
        if len(os.listdir(game_dir)) < 2:
            continue

        game_page_path = os.path.join(game_dir, 'page.html')

        with open(game_page_path, 'r') as f:
            page = f.read()

        #game_name = re.search('<title>(.*) скачать бесплатно на телефон</title>', page)
        #game_name = game_name.group(1)
        ## extracting game info
        #m = re.search('\d+</a> <br/><br/>(.*)<b>Загрузил', page, re.DOTALL)

        #if m:
            #game_info = strip_tags(m.group(1))
        #else:
            #continue
        #    print('!!!!!!!!!!!!!NONE!!!!!!!!!!!!!!!!!!!')
        m = re.findall('<font color="#"><hr/></font>([\S\s]*?)<br/><a class="dwn_data" href="/game/(\d*)/', page)

        for link in m:
            game_file = os.path.join(game_dir, link[1] + '.jar')

            # is game info standard
            if os.path.exists(game_file):
                gamefile_specifications = link[0].strip()

                # screen resolution
                screen = re.search('^\d{3}x\d{3}', gamefile_specifications)

                # game language (eng/ru)
                lang = re.search('ENG|Eng|eng|RUS|Rus|rus|EN|En|en|RU|Ru|ru', gamefile_specifications)

                new_name = ''

                if screen:
                    new_name = screen.group() + '_'
                if lang:
                    new_name += lang.group(0) + '_'

                #tmp = link[0].replace(',', '_')
                #tmp = tmp.replace('/', '_')
                #tmp_name = tmp.split()
                print(new_name)
                exit()

                #if len(old_name) < 4:
                    #print(game_page_path)
                    #new_name = old_name[0] + '_' + old_name[2]
                #else:
                    #new_name = old_name[0] + '_' + old_name[2] + old_name[3]

                    #if len(new_name) > 20:
                        #new_name = new_name[:20]

                    #new_name = new_name + '_' + old_name[-1] + '.jar'
                    #new_name_path = os.path.join(game_dir, new_name)

                ## write game_id to directory for future use
                #with open(os.path.join(game_dir, game_id), 'w') as f:
                    #f.write('')

                # rename gamefile
#                os.rename(game_file, new_name_path)
#            else:
#                print(game_name, game_file)
        # rename gamedirectory from id to normal name
#        new_game_dir = os.path.join(cat_games_dir, game_name)
#        shutil.move(game_dir, new_game_dir)
    return


def main():
    for cat in categories:
        parse_games(cat)
    return


if __name__ == "__main__":
    main()
