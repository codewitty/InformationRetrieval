import json
import os
from bs4 import BeautifulSoup


def print_words(filename):
    f = open(filename)
    data = json.load(f)
    print(data['url'])


def enter(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file

        if os.path.isfile(f):
            print_words(f)
            enter(f)



if __name__ == '__main__':
    directory = 'desktop//analyst'
    enter(directory)
    