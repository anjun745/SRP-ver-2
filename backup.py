import requests
from bs4 import BeautifulSoup

MEANING_MAP = {}


def main():
    """ 
    Scraping :D
    tell the program the url of your search, if it is google search that is >.>
    prints what you searched
    Inputs:
        the url of a google search

    Outputs:
        prints out what you searched
    """
    words = [input("The starting word, enter blank to stop: ")]
    generation_count = 3
    for i in range(generation_count):
        next_gen = []
        for word in words:
            url = 'https://www.google.com/search?q=definition%20of%20' + word + '&ie=utf-8&oe=utf-8'
            req = requests.get(url=url)
            soup = BeautifulSoup(req.content, 'html.parser')
            # search = soup.find_all(attrs={"class": "r0bn4c rQMQod"})  # take into account that if it isn't shown as
            # the typical google format, it needs to be skipped
            search = soup.find_all("span", class_="r0bn4c rQMQod")
            # print(url)
            # print(search)
            for s in search:
                if "synonyms: " in str(s):
                    for syn in s.text.split(": ")[1].split(", "):
                        MEANING_MAP.setdefault(word, []).append(syn)
                        MEANING_MAP.setdefault(syn, [word])
                    next_gen += s.text.split(": ")[1].split(", ")
            try:
                MEANING_MAP[word] = list(set(MEANING_MAP[word]))
            except KeyError:
                print("failed to find word")
                pass
        words = next_gen
        print(f"Gen: {i}, Len: {len(MEANING_MAP)}")
        # word = input("The starting word, enter blank to stop: ")


# This provided line is required at the end of a Python file
# to call the main() function.
if __name__ == '__main__':
    main()
    print(MEANING_MAP.keys())
