import pandas as pd
from preprocessing import clean_stopwords, clean_punctuation, tokenize
from embeddings import make_word_embedding
from extract_features import extract_features
import os

train_folder = '/Users/lenka/Desktop/work/train'
test_folder = '/Users/lenka/Desktop/test'


def load_data(file_path):
    loaded_data = pd.read_csv(file_path, sep='\t', header=None)
    add_column_names(loaded_data)

    return loaded_data


def load_test_set(lang):
    global test_folder
    test_data = load_data(test_folder+'/'+lang+'.tsv')

    tokenized_data = tokenize(test_data, lang)
    clean_data = clean_punctuation(tokenized_data)
    clean_data = clean_stopwords(clean_data, lang)

    embedding = make_word_embedding(clean_data,lang)
    features = extract_features(clean_data, [], lang, embedding)
    print('extracted features for', lang, len(clean_data))
    return features


def add_column_names(df):
    if len(df.columns) == 5:
        column_names = ['word', 'pos', 'def1', 'def2', 'relation']
    else:
        column_names = ['word', 'pos', 'def1', 'def2']
    df.columns = column_names


def undersample_dataset(imbalanced_set):
    none = imbalanced_set[has_label(imbalanced_set, 'none') == True]
    second_biggest = imbalanced_set.groupby('relation').count().word.sort_values(ascending=False)[1]
    result = imbalanced_set.drop(none.index[second_biggest:])

    return result.sample(frac=1, random_state=7)


def sort(lst):
    return sorted(lst, key=len)


def filter_small_length(dataset, threshold):
    return len(dataset.index) > threshold


def categorize_by_label(df):
    relation_labels = df['relation'].unique()
    smallest_by_label = {}
    for relation in relation_labels:
        smallest_by_label[relation] = df[has_label(df, relation)]

    return smallest_by_label


def upsample_from_bigger_set(smallest_by_label, bigger_by_label):
    biggeset_label, biggest_label_size = find_biggest_label_and_size(smallest_by_label)

    return upsample_by_diff(bigger_by_label, biggeset_label, biggest_label_size, smallest_by_label)


def upsample_by_diff(bigger_by_label, biggeset_label, biggest_label_size, smallest_by_label):
    for key in smallest_by_label:
        if key != biggeset_label:
            diff = biggest_label_size - len(smallest_by_label[key].index)
            if diff > 0:
                new_data = bigger_by_label[key].sample(n=diff, random_state=7, replace=True)
                smallest_by_label[key] = smallest_by_label[key].append(new_data)

    return smallest_by_label


def find_biggest_label_and_size(smallest_by_label):
    largest_label = None
    largest_label_size = 0

    for key in smallest_by_label:
        if len(smallest_by_label[key].index) > largest_label_size:
            largest_label_size = len(smallest_by_label[key].index)
            largest_label = key

    return largest_label, largest_label_size


def sort_dataset(all_data, dataset_lang):
    lang_data = []
    for key in all_data.keys():
        if dataset_lang in key:
            lang_data.append(all_data[key])
    sorted_sets = list(filter(lambda elem: filter_small_length(elem, 100), sort(lang_data)))
    return sorted_sets

def combine_labels(dict_by_label):
    df = pd.DataFrame()

    for key in dict_by_label:
        df = df.append(dict_by_label[key])

    return df.sample(frac=1, random_state=7)


def balance_dataset(sorted_sets, balancing):
    if balancing == 'undersampling':
        result = undersample_dataset(sorted_sets[0])

    else:
        # print(sorted_sets)
        print(len(sorted_sets))
        smallest = sorted_sets[0]
        # bigger = sorted_sets[1]

        smallest_by_label = categorize_by_label(sorted_sets[0])

        result = combine_labels(upsample_from_bigger_set(smallest_by_label, smallest_by_label))

    return result



def load_training_data(folder):
    combined_set = {}

    for filename in os.listdir(folder):
        if filename.endswith(".tsv"):
            combined_set[filename.split('.')[0]] = load_data(folder + '/' + filename)

    return combined_set


def load_and_preprocess(dataset_lang, balancing):
    global train_folder
    all_data = load_training_data(train_folder)
    sorted_sets = sort_dataset(all_data, dataset_lang)

    print('sorted', len(sorted_sets))

    balanced = balance_dataset(sorted_sets, balancing)

    print('balanced', len(balanced))

    tokenized =  tokenize(balanced, dataset_lang)
    clean = clean_punctuation(tokenized)
    clean = clean_stopwords(clean, dataset_lang)

    return clean


def has_label(df, label):
    return df['relation'] == label




