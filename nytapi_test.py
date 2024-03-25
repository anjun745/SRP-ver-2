import requests
import json
import speech_recognition

KEY1 = 'moUvPrJipxItIw4bLsv9wkjyuyJZqvVL'
KEY2 = '0mP08dG2n0R8J7mCeB0pScYofeEgyh4K'

url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key=" + KEY2
req = requests.get(url)
js = json.loads(req.content)
# print(js)
for k in js['response']['docs'][1]:
    print(k)
print(js['response']['docs'])
