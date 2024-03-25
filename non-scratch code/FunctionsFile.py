# will probably serve as a function folder
# use the plk trained file to generate

from bs4 import BeautifulSoup
import string
import json
import requests
import random as rand
import re

KEY_T = "66d293ef-56a2-48c9-9e14-201929f235ee"
KEY_D = "a17b1c91-58d4-43c0-baae-2104dd1c8286"
BOOK = "bookoffate.txt"


def find_word_single(word: str, key=KEY_T):
    """
    To look up a single word and get the relevant information,
    such as syns, ants, and tense (noun, adj, verb)
    :param key: API Key
    :param word: the word being searched
    :return: relevant information in the form of a list
    """
    # since this gives the stems, I will have to backtrack... FUCKK
    info = {"syn": [], "ant": [], "stems": [], "pos": "noun", 'short_def': '', 'wd': []}
    url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + key
    req = requests.get(url=url)
    try:
        js = json.loads(req.content)
        if len(js) and type(js[0]) == dict:
            info['pos'] = js[0]['fl']
            info['short_def'] = js[0]['shortdef']
            info['syn'] = js[0]['meta']['syns']
            info['ant'] = js[0]['meta']['ants']
            info['stems'] = js[0]['meta']['stems']
    except json.decoder.JSONDecodeError:
        pass
    return info


def get_text(word, text):
    """
    gets the sentences from text
    :param word: the word to be searched up
    :param text: the text to search
    :return: the sentences with the words
    """
    sentences = []
    # 1. get the sentences with such words. Will be difficult
    # 1.1 need to get the punctuations (' excluded) to find start and end
    with open(text) as f:
        text = f.read()
    try:
        locs = [i.start() for i in re.finditer(word, text)] + [i.start() for i in re.finditer(word.capitalize(), text)]
    except re.error:
        locs = []
    for word in locs:  # word is the start index
        start, end = None, None
        for start in range(word, 0, -1):
            if text[start] in string.punctuation and text[start] != "'":
                break
        for end in range(word, word+450):
            if text[end] in string.punctuation and text[end] != "'":
                break
        if start and end:
            sentences.append(text[start:end+1])
    return sentences


def word_relations(word, texts: list):
    """
    finds the relation between words (before/after certain words, certain patterns)
    for markov chain
    :param word: the word which relations are made for
    :param texts: the text searching
    :return: related words from text
    """
    related = []  # weighted list
    for example in texts:
        example = example.split()
        for w in example:
            if w != word and w != word.capitalize() and w not in string.punctuation:
                related.append(w.strip(string.punctuation))
    return {word: related}


def markov_dict(word, texts):
    """
    to create something for the markov chain to select
    will be called for every unique word
    will be needing global var, and use the result from get_text
    :param word: the word that is being checked if something needs to be created
    :param texts: the texts that contains the word
    :return: a dictionary of words and what comes after (weighted)
    """
    # 0. get the result from get_text
    # 1. split up for same sentence words and directly following (or punctuations)
    # 2. store it
    behind = []
    for example in texts:
        i = example.lower().find(word.lower())
        example = example[i::].split()
        if not example:
            pass
        elif example[0][-1] in string.punctuation and example[0][-1] != '\\':
            behind.append(example[0][-1])
        if len(example) > 1:
            behind.append(example[1])
    return {word: behind}


def markov_select(seqs, prev: str = None):
    """
    Selects a word to follow, or end a sentence on
    :param seqs: the sequence for words
    :param prev: The word previous, default to None
    :return: The chosen word
    """
    try:
        return rand.choice(seqs[prev])
    except IndexError:
        return ''


if __name__ == '__main__':
    d = get_text('gold', BOOK)
    print(markov_dict('gold', d))
