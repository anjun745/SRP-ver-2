import requests
from bs4 import BeautifulSoup
import json

KEY_T = "66d293ef-56a2-48c9-9e14-201929f235ee"
KEY_D = "a17b1c91-58d4-43c0-baae-2104dd1c8286"
MEANING_MAP = {}


def main():
    words = [input("The starting word, enter blank to stop: ")]
    generation_count = 1
    for i in range(generation_count):
        print(f"---- \n\n\n {i} \n\n\n ---")
        next_gen = []
        for word in words:
            url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + KEY_T
            req = requests.get(url=url)
            # soup = BeautifulSoup(req.content, 'html.parser')
            js = json.loads(req.content)
            # js[<index>]['meta']['syns'] will always be a list of lists
            if len(js) and type(js[0]) == dict:
                for usage in js:
                    for words_ in usage['meta']['syns']:
                        for word_ in words_:
                            # might need more classification later on
                            MEANING_MAP.setdefault(word, []).append(word_)
                            MEANING_MAP.setdefault(word_, []).append(word)
                            MEANING_MAP[word_] = list(set(MEANING_MAP[word_]))
                            MEANING_MAP[word] = list(set(MEANING_MAP[word]))
                            print(len(MEANING_MAP))
                            next_gen.append(word_)
            else:
                print(word)
                pass
        words = list(set(next_gen))


if __name__ == '__main__':
    main()
    print(MEANING_MAP)