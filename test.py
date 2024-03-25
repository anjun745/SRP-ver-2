"""
the following program has been successful as of 29/Nov/2020
Completed:
Allow support for multiple word inputs

On-going:
Proceeding to --> Adding a timer to allow timed stopping

Next up:
Work on NYT api
Saving to json or some other data format
"""

# from bs4 import BeautifulSoup   # not needed as of right now
import requests
import json

KEY_T = "66d293ef-56a2-48c9-9e14-201929f235ee"
KEY_D = "a17b1c91-58d4-43c0-baae-2104dd1c8286"
MEANING_MAP_SYN = {}
MEANING_MAP_ANT = {}
WORD_TYPE = {}


def adding_words(words, loc: dict, nxt_g: set, w):
    """
    adds words to the dictionaries, in here known as 'loc' and the sets known as 'next_g'
    :param nxt_g: adds to the next gen set
    :param words: the words array
    :param loc: the set of which is being added to
    :param w: the original word
    :return: Nothing, just adds to the array
    """
    for w_ in words:
        loc.setdefault(w, set()).add(w_)  # adding paths both ways
        loc.setdefault(w_, set()).add(w)
        nxt_g.add(w_)  # for next gen


def exploration(word_set: set, nxt_g: set, url_: tuple):
    """
    keeps looping through the set until no worlds are left, and the next_gen will gain more words
    :param word_set: current word set
    :param nxt_g: next generation set
    :param url_: the url formatted to allow the word and keys to be combined in
    :return: the amount of words for the next generation
    """
    while word_set:
        word = word_set.pop()
        url = url_[0] + word + url_[1] + KEY_T
        req = requests.get(url=url)
        js = json.loads(req.content)
        # js[<index>]['meta']['syns'] will always be a list of lists
        if len(js) and type(js[0]) == dict:
            for usage in js:  # different variations
                WORD_TYPE.setdefault(word, set()).add(usage['fl'])  # probably a str
                for words_ in usage['meta']['syns']:  # could make these 2 shorter
                    adding_words(words_, MEANING_MAP_SYN, nxt_g, word)
                for words_ in usage['meta']['ants']:
                    adding_words(words_, MEANING_MAP_ANT, nxt_g, word)
            print(len(MEANING_MAP_ANT), 'ant')
            print(len(MEANING_MAP_SYN), 'syn')
        else:
            print(word)  # if the word's js has len of 0 and/or the js isn't starting with a dict
            pass
    return nxt_g


def main():
    words = set(input("The starting words separate by space, enter blank to stop program: ").split())
    generation_count = int(input('how many generations (Warning, it gets a lot longer with each gen): '))
    next_gen = set()
    for i in range(generation_count):
        print(f"----\n\n\n gen {i} \n\n\n----")
        exploration(words, next_gen,
                    ("https://www.dictionaryapi.com/api/v3/references/thesaurus/json/", "?key="))  # insert word between
        words = next_gen.copy()
        next_gen.clear()
    # cleaning up/final batch
    exploration(words, next_gen,
                ("https://www.dictionaryapi.com/api/v3/references/thesaurus/json/", "?key="))


if __name__ == '__main__':
    main()
    print('--------------Syn--------------')
    print(MEANING_MAP_SYN)
    print('--------------Ant--------------')
    print(MEANING_MAP_ANT)
    print('--------------Typ--------------')
    print(WORD_TYPE)
