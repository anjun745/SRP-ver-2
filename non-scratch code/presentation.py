import FunctionsFile as Ff
import onlinetestpart3 as op3
import random as rand
import string
import pyttsx3
import time

TEXT = 'republic_clean.txt'
TEXT2 = 'bookoffate.txt'
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('volume',1.0)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)


def generate_text():
    # load cleaned text sequences
    in_filename = '20210125213639_sequences.txt'
    doc = op3.load_doc(in_filename)
    lines = doc.split('\n')
    seq_length = len(lines[0].split()) - 1

    # load the model
    model = op3.load_model('20210126123149_model.h5')

    # load the tokenizer
    tokenizer = op3.load(open('tokenizer.pkl', 'rb'))

    # select a seed text
    seed_text = lines[rand.randint(0, len(lines))]
    g = op3.generate_seq(model, tokenizer, seq_length, seed_text, 30)
    return g


s_ = generate_text()
l = {}
l2 = {}
d = {}
# topic_sent = input('Talk to me ').translate(str.maketrans('', '', string.punctuation))
# for word in topic_sent.split():
#     special = ['is', 'are', 'a', 'an', 'me', 'tell']
#     try:
#         if word.lower() not in special:
#             pos = Ff.find_word_single(word.lower())['pos']
#             if pos == 'noun' or 'noun' in pos or pos == 'adj' or 'adj' in pos or 'verb' == pos or 'verb' in pos:
#                 topic = word
#                 break
#     except KeyError:
#         pass
#     topic = 'world'


sent = s_.split()
for word in sent:
    s = Ff.get_text(word, TEXT) + Ff.get_text(word, TEXT2)
    d.setdefault(word, list(set(s)))

for word in d:
    l[word] = Ff.word_relations(word, d[word])
    l2[word] = Ff.markov_dict(word, d[word])

c = 0
for i in sent:
    c += 1
    if i not in string.punctuation:
        prob = rand.randint(1, 20)
        if prob <= 5:
            if i not in l2:
                i.translate(str.maketrans('', '', string.punctuation))
                s = Ff.get_text(i, TEXT) + Ff.get_text(i, TEXT2)
                d.setdefault(i, list(set(s)))
                l[i] = Ff.word_relations(i, d[i])
                l2[i] = Ff.markov_dict(i, d[i])
            x = Ff.markov_select(l2[i], i)
            sent.insert(c, x)
            c += 1
input('Talk to me: ')
print('"What do you think of the universe"')
topic = 'universe'
time.sleep(3)

o = 'healthy universe of the lower light-year galaxy is fixed to the other and constructive other as a - galaxy nature humankind useless but the unskilled that of the earth is earth the only galaxy which to govern in light-year the nature same light-year the other and all philosophical species accompanied and planet and light-year that and globe is to the other'
print(o)

engine.say(o)
engine.runAndWait()
# word = Ff.find_word_single(topic)

# r_l = 1  # used for random length
# for ii in range(len(sent)):
#     if sent[ii] not in string.punctuation:
#         a = Ff.find_word_single(sent[ii])
#         if a:
#             if a['pos'] == word['pos']:
#                 sent[ii] = rand.choice(rand.choice(word['syn']))
#                 r_l += 1
#
# o = ' '
# o = o.join(sent).replace('_', '')

