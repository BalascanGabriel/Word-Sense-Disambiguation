
from lesk import lesk


def load_test_set(filename):
    dataset = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        tokens = line.split(',')
        if len(tokens) < 3:
            continue
        dataset.append({'word': tokens[0],
                        'sentence': tokens[1].replace('\"', ''),
                        'correct_synset_id': tokens[2]})
    return dataset


def main():
    dataset = load_test_set('testSet.txt')
    results = {}
    for example in dataset:
        results[example['word']] = {'correct': 0,
                                    'wrong': 0,
                                    'total': 0}
    for example in dataset:
        synset = lesk(example['word'], example['sentence'])
        if synset == example['correct_synset_id']:
            results[example['word']]['correct'] += 1
            print('Correct: ' + example['sentence'])
        else:
            results[example['word']]['wrong'] += 1
            print('Wrong: ' + example['sentence'])
        results[example['word']]['total'] += 1

    total_correct = 0
    total_total = 0
    for key, val in results.items():
        total_correct += results[key]['correct']
        total_total += results[key]['total']

    for key, val in results.items():
        print('Accuracy for word \"' + key + '\": ' + str(results[key]['correct']/results[key]['total'] * 100) + '%')

    print('\nOverall accuracy: ' + str(total_correct/total_total * 100) + '%')


if __name__ == '__main__':
    main()
