import FunctionsFile as Ff
import onlinetestpart3 as op3
import random as rand
import string
import plottingsocre as pscore

# s_ = 'we were saying that the soul is not this art is also the same and the same faculty cannot be destroyed as that is the same and the other and the same are the same and the unjust may be explained in the state and not to be cured and'
# s_ = 'to say that the just man is not that we were starting to war and cannot be tested by the good and opinions of the state and the same and the same faculty i should say that the soul of the individual is not the same and the same faculty'
TEXT = 'republic_clean.txt'
TEXT2 = 'bookoffate.txt'


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
    # print(seed_text + '\n')
    # print('---')
    # generate new text
    generated = op3.generate_seq(model, tokenizer, seq_length, seed_text, 50)
    return generated


s1l = []
s2l = []
s3l = []
# topics = ['world', 'joy', 'eat', 'hope']
topics = ['world']
for topic in topics:
    print(topic)
    for loop in range(1):
        print(loop)
        l = {}
        l2 = {}
        d = {}
        # topic = input('what is the topic? ')
        s_ = generate_text()
        print(s_)
        sent = s_.split()
        # print('text generated')
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
                prob = rand.randint(1, 10)
                if prob <= 3:
                    if i not in l2:
                        i.translate(str.maketrans('', '', string.punctuation))
                        s = Ff.get_text(i, TEXT) + Ff.get_text(i, TEXT2)
                        d.setdefault(i, list(set(s)))
                        l[i] = Ff.word_relations(i, d[i])
                        l2[i] = Ff.markov_dict(i, d[i])
                    x = Ff.markov_select(l2[i], i)
                    sent.insert(c, x)
                    c += 1
        # print('format complete, adding context')

        word = Ff.find_word_single(topic)
        r_l = 1  # used for random length
        for ii in range(len(sent)):
            if sent[ii] not in string.punctuation:
                a = Ff.find_word_single(sent[ii])
                if a:
                    if a['pos'] == word['pos']:
                        sent[ii] = rand.choice(rand.choice(word['syn']))
                        r_l += 1

        # print(sent)
        o = ' '
        o = o.join(sent)
        print(o)
        sect = rand.choice(word['syn']) + rand.choices(s_.split(), k=r_l)
        print(sect)
        r_ = o.split()[:int(len(s_) * 0.8)]
        r = ' '
        rand.shuffle(r_)
        r = r.join(r_)
        r.translate(str.maketrans('', '', string.punctuation))
        # print(r)
        il = len(sent)
        # print('scoring')
        s1, s2 = pscore.scoring(o, context=topic, ideal_l=il), pscore.scoring(s_, context=topic, ideal_l=il)
        s3 = pscore.scoring(r, context=topic, ideal_l=il)
        s1l.append(s1)
        s2l.append(s2)
        s3l.append(s3)
    # print('done')

print('plotting')
pscore.plotting([s1l, s2l, s3l], hist=True)
pscore.plotting([s1l, s2l, s3l])
