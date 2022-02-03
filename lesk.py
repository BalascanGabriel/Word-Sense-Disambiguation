from nltk.stem import SnowballStemmer
import pandas as pd
import rowordnet as rwn
import re
import sys


def scan_line(line, regx, stemmer):  # extrag cuvintele din propozitie, si le marchez prezenta prin valoarea 1
    wordset = {}
    strings = regx.split(line)
    for str in strings:
        size = len(str)
        if size <= 1:
            continue
        else:
            str = stemmer.stem(str)
            wordset[str] = 1
    return wordset


def compute_overlap(signature, context):  # Calculez apropierea dintre contextul propozitiei mele si semnatura sensului
    overlap = 0
    for word, val in signature.items():
        v = context.get(word, 0)
        if v != 0:
            overlap = overlap + 1
    return overlap


def lesk(word, sentence):  # Apelez algoritmul lesk
    stemmer = SnowballStemmer("romanian")
    regx = re.compile("[^a-zA-ZșțȘȚăîâĂÂÎ]")
    wn = rwn.RoWordNet()
    dataset = pd.read_pickle('dataset.pickle')

    context = scan_line(sentence, regx, stemmer)
    senses = wn.synsets(word)
    if len(senses) > 0:
        max_overlap = -1
        result = ''
        synset_id = senses[0]
        for s in senses:  # verific fiecare sens posibil pentru cuvant
            synset = wn.synset(s)
            info = synset.definition + ' '  # incep sa formez semnatura sensului, adaugand initial definitia acestuia
            for key, entries in dataset.items():
                if key != word:
                    continue
                for entry in entries:
                    if entry['correct_synset_id'] == s:
                        info = info + entry['sentence'] + ' '  # daca in setul de date din pickle imi apare un
                        # exemplu cu acelasi sens, il concatenez la semnatura

            signature = scan_line(info, regx, stemmer)  # extrag cuvintele in forma redusa care apar in semnatura
            overlap = compute_overlap(signature,
                                      context)  # verific cate cuvinte se repeta intre context si semnatura sensului
            if overlap > max_overlap:  # salvez definitia sensului cu cel mai mare overlap intre context si semnatura
                max_overlap = overlap
                result = synset.definition
                synset_id = s

        print('Result is: ' + result)
        print('Sense ' + synset_id)
        return synset_id
    else:
        print('Word not known!')
        return None


def main():
    if len(sys.argv) != 3:
        print("Usage: python lesk.py word sentence")
        sys.exit(0)

    lesk(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
