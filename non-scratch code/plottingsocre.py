import matplotlib.pyplot as plt
import FunctionsFile as Ff
import string
import language_check
from lark import lark
import numpy as np
from datetime import datetime


def scoring(sent, context, ideal_l=50):
    """

    :param sent: the sentence
    :param ideal_l: ideal length
    :param context: the word of context
    :return: a score for the sentence
    """
    c = Ff.find_word_single(context)
    word_in = 0.1
    word_tot = 0.1
    p = 0
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(sent)
    gr = 0.97**len(matches)
    for s in sent.split():
        if s not in string.punctuation:
            s.translate(str.maketrans('', '', string.punctuation))
            s_info = Ff.find_word_single(s)
            if s_info:
                if s_info['pos'] == c['pos']:
                    for ssyn in s_info['syn']:
                        for csyn in c['syn']:
                            if s in csyn or context in ssyn:
                                word_tot += 1
                                word_in += 1
                            else:
                                word_tot += 1
        else:
            p += 0.075
    return (word_in/word_tot)*(p + gr)*(0.99**(abs(ideal_l-len(sent))))*10


def plotting(scores, hist=False):
    """
    for plotting
    :param scores: either for dot plots or histograms
    :param hist: determines if the plot is a histogram or not
    :return:
    """
    fig = plt.figure()
    if hist:
        s = []
        for s_ in scores:
            s.append(np.mean(s_))
        types = ['NLP + ML', 'ML', "NLP"]
        plt.bar(types, s, label=['NLP + ML', 'ML', "NLP"])
        plt.title("Average score comparison")
        plt.ylabel('Score')
        n = f"{str(datetime.now()).replace(':', '').replace('.', '').replace(' ', '').replace('-', '')[:-6]}" \
            f"_hist.png"
    else:
        for s in scores:
            plt.plot(s, '.')
        plt.legend(['NLP + ML', 'ML', "NLP"])
        plt.xlabel('Trial number')
        plt.ylabel('Score')
        plt.title("Individual score comparison")
        n = f"{str(datetime.now()).replace(':', '').replace('.', '').replace(' ', '').replace('-', '')[:-6]}" \
            f"_dot.png"
    plt.show()
    fig.savefig(n, bbox_inches='tight')
    return


if __name__ == "__main__":
    s = 'of the galaxy and not to be allowed and when globe has a winning enquiry have been been folks of species in which the light-year are say, to be expected to do with the same universe to the galaxy arrive shaking earth light-year at creation the galaxy of hephaestus in actual earth the globe ,'
    print(scoring(s, 'world'))
