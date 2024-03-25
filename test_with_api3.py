import requests
from bs4 import BeautifulSoup
import json

KEY_T = "66d293ef-56a2-48c9-9e14-201929f235ee"
KEY_D = "a17b1c91-58d4-43c0-baae-2104dd1c8286"
PARTS_OF_SPEECH = {}
MEANING_MAP = {}  # will change this later to be read from the json
SUB_LIST = ['die']


def main():
    # for word in MEANING_MAP:
    for word in SUB_LIST:
        url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + KEY_T
        req = requests.get(url=url)
        js = json.loads(req.content)
        if len(js) and type(js[0]) == dict:
            for usage in js:
                print(usage['fl'])


if __name__ == '__main__':
    main()
