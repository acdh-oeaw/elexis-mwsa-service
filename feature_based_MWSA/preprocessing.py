import stop_words
import nltk
from spacy.tokenizer import Tokenizer
from spacy.lang.ru import Russian
from spacy.lang.es import Spanish
from spacy.lang.it import Italian
from spacy.lang.en import English
from spacy.lang.de import German
from spacy.lang.nl import Dutch
from spacy.lang.hu import Hungarian
from spacy.lang.ga import Irish


stopwords = {}

spacies = {'russian': Russian(), 'spanish': Spanish(), 'italian':Italian(), 'english': English(),
           'german': German(), 'dutch': Dutch(), 'hungarian': Hungarian(), 'irish': Irish()}

tokenizers = {}

for lang in spacies:
    tokenizers[lang] = Tokenizer(spacies[lang].vocab)

def load_stopwords():
    global stopwords
    folder_st = 'data/stopwords/'
    languages = ['basque','bulgarian','estonian',
                 'hungarian','italian','irish','portuguese',
                 'russian','serbian','slovene','danish','dutch'] #add spanish

    for lang in languages:
        if lang in ['basque', 'estonian', 'irish', 'slovene', 'serbian']:
            filename = folder_st + lang + '.txt'
            # print(filename)
            file = open(filename, 'r')
            st = file.read()
            if lang == 'serbian':
                st_list = st.split('\n')
            else:
                st_list = st.replace('[', '').replace(']', '').replace('"', '').split(',')
        else:

            st_list = stop_words.get_stop_words(lang)

        print(lang, len(st_list))
        stopwords[lang] = st_list

    return stopwords

load_stopwords()


def get_tokens(definition, lang):
    if lang in spacies:
        tok = tokenizers[lang].tokenize(definition)
    else:
        tok = nltk.tokenize.word_tokenize(definition)

    return tok

def remove_punctuation(tokenized_definition):
    cleandef = ''
    for word in tokenized_definition.replace('[','').replace(']','').replace('\'','').split(','):
        if word.isalpha():
            cleandef += ' ' + word.lower()
            # print(word)
    if cleandef == '':
        return tokenized_definition.lower()
    return cleandef.strip()


def clean_punctuation(dataset):
    for index, row in dataset.iterrows():
        dataset.at[index, 'def1_clean'] = remove_punctuation(row['def1_tokenized'])
        dataset.at[index, 'def2_clean'] = remove_punctuation(row['def2_tokenized'])
    return dataset


def remove_stopwords(definition, lang):
    cleandef = ''
    for word in definition.split():
        if word not in stopwords[lang]:
            cleandef += ' ' + word
    if cleandef == '':
        return definition
    #print(cleandef)
    return cleandef.strip()


def clean_stopwords(dataset, lang):
    for index, row in dataset.iterrows():
        dataset.at[index, 'def1_stop'] = remove_stopwords(row['def1_clean'], lang)
        dataset.at[index, 'def2_stop'] = remove_stopwords(row['def2_clean'], lang)
    return dataset


def tokenize(dataset, lang):

    for index, row in dataset.iterrows():
        dataset.at[index, 'def1_tokenized'] = str(get_tokens(row['def1'], lang))
        dataset.at[index, 'def2_tokenized'] = str(get_tokens(row['def2'], lang))
    return dataset
