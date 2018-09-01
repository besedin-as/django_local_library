from nermaster.ner.utils import download_untar


conll_tar_url = 'http://lnsigo.mipt.ru/export/datasets/conll2003.tar.gz'
download_path = 'conll2003/'
download_untar(conll_tar_url, download_path)

data_types = ['train', 'test', 'valid']
dataset_dict = dict()
for data_type in data_types:

    with open('conll2003/' + data_type + '.txt') as f:
        xy_list = list()
        tokens = list()
        tags = list()
        for line in f:
            items = line.split()
            if len(items) > 1 and '-DOCSTART-' not in items[0]:
                token, tag = items
                if token[0].isdigit():
                    tokens.append('#')
                else:
                    tokens.append(token)
                tags.append(tag)
            elif len(tokens) > 0:
                xy_list.append((tokens, tags,))
                tokens = list()
                tags = list()
        dataset_dict[data_type] = xy_list

for key in dataset_dict:
    print('Number of samples (sentences) in {:<5}: {}'.format(key, len(dataset_dict[key])))

print('\nHere is a first two samples from the train part of the dataset:')
first_two_train_samples = dataset_dict['train'][:2]
for n, sample in enumerate(first_two_train_samples):
    # sample is a tuple of sentence_tokens and sentence_tags
    tokens, tags = sample
    print('Sentence {}'.format(n))
    print('Tokens: {}'.format(tokens))
    print('Tags:   {}'.format(tags))