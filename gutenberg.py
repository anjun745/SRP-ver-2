import requests
import string
import json

url = 'https://www.gutenberg.org/cache/epub/2701/pg2701.txt'
req = requests.get(url=url)
words = str(req.content).replace('\\r', '').replace('\\n', '')
words_order = words[:words.find('End of Project Gutenberg')].split()


def make_clean_copy(words_str):
    w = words.replace('--', ' ')
    t = w.split()
    t = [w.translate(str.maketrans('', '', string.punctuation)) for w in t]
    t = [word for word in t if word.isalpha()]
    t = [word.lower() for word in t]
    return t


tokens = make_clean_copy(words_order)
uc = len(set(tokens))
wc = len(tokens)

length = 50 + 1
seq = []
for i in range(length, len(tokens)):
    s = tokens[i-length:i]
    line = ' '.join(seq)
    seq.append(line)
