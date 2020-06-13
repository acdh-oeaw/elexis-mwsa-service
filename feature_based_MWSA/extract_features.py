import numpy as np
import pandas as pd
import preprocessing, embeddings
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def first_word_same(row):
    return row['def1_clean'].split(' ')[0].lower() == row['def2_clean'].split(' ')[0].lower()


def difference_in_length(row):
    return abs(len(row['def1_clean'].split(' ')) - len(row['def2_clean'].split(' ')[0]))


def jaccard_sim(row):
    return get_jaccard_sim(row['def1_clean'], row['def2_clean'])


def cos_gensim(row, lang, embedding=None):
    # unpack tokens from string
    def1 = row['def1_tokenized'].replace('[','').replace(']','').replace('\'','').split(',')
    def2 = row['def2_tokenized'].replace('[','').replace(']','').replace('\'','').split(',')

    cg = get_cos_gensim(def1, def2, lang, embedding) #with stopwords
    if type(cg) == int:
        return cg
    return cg[0, 1]



def get_cos_gensim(tokenized_def1, tokenized_def2, lang, embedding=None):
    if embedding == None:
        embedding = embeddings.embeddings[lang]

    avg1 = []
    for word in tokenized_def1:
        if word in embedding:
            avg1.append(embedding[word])
            # else ?

    avg2 = []
    for word in tokenized_def2:
        if word in embedding:
            avg2.append(embedding[word])

    v1 = np.array(avg1).reshape(-1, 1)
    v2 = np.array(avg2).reshape(-1, 1)

    if len(v1) == 0 or len(v2) == 0:
        print('zero vector')
        return 0

    return cosine_similarity(v1, v2)


def wmd(row, lang, embedding=None):
    # unpack tokens from string
    def1 = row['def1_tokenized'].replace('[','').replace(']','').replace('\'','').split(',')
    def2 = row['def2_tokenized'].replace('[','').replace(']','').replace('\'','').split(',')
    return get_wmd(lang, def1, def2) #still has stopwords


def get_wmd(lang, tokenized_def1, tokenized_def2, embedding=None):
    if embedding:
        return embedding.wmdistance(tokenized_def1, tokenized_def2)

    return embeddings.embeddings[lang].wmdistance(tokenized_def1, tokenized_def2)


def cosine(row):
    cos = get_cosine_sim(row['def1_stop'], row['def2_stop'])
    return cos[0, 1]


def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)


def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()


# TODO LEMMA
def root_same(row, lang):
    return root_word_same(row['def1_clean'], row['def2_clean'], lang)

import nlp_pipelines

def root_word_same(def1, def2, lang):
    root1 = ''
    root2 = ''

    doc1 = nlp_pipelines.pipelines[lang](def1)
    doc2 = nlp_pipelines.pipelines[lang](def2)

    for token in doc1.sentences[0].tokens:
        if token.words[0].dependency_relation == 'root':
            root1 = token.words[0].lemma
            break

    for token in doc2.sentences[0].tokens:
        if token.words[0].dependency_relation == 'root':
            root2 = token.words[0].lemma
            break

    # print(root1, root2, root1==root2)
    return root1 == root2

from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf(col1, col2):
    tfidf_holder = pd.DataFrame()
    tfidf_holder['col1'] = col1
    tfidf_holder['col2'] = col2

    values = join_definitions(col1, col2)
    #print('val', values)
    tfidf_holder['tfidf_1'], tfidf_holder['tfidf_2'] = tfidf_vectors(values)

    return tfidf_holder.apply(lambda row: cosine_similarity([row['tfidf_1'], row['tfidf_2']])[0, 1], axis=1)


def convert_to_text(token_array):
    seperator = ' '
    return seperator.join(token_array)


def join_definitions(col1, col2):
    joined_definitions = pd.concat([col1, col2])
    return joined_definitions.values.T #.apply(lambda tokens: ' '.join(tokens)).values.T


def tfidf_vectors(values):
    tfidf_matrix = TfidfVectorizer().fit_transform(values)

    split_index = int(tfidf_matrix.get_shape()[0] / 2)
    tfidf_array = tfidf_matrix.todense()

    df_result1 = [row.tolist()[0] for row in tfidf_array[0:split_index]]
    df_result2 = [row.tolist()[0] for row in tfidf_array[split_index:]]

    return df_result1, df_result2


def extract_features(data, feats_to_scale, lang, embedding=None):
    # def sentence2vec(row):
    #    return row['processed_1'].similarity(row['processed_2'])

    feat = pd.DataFrame()
    # print(data)
    # feat['similarities'] = data.apply(lambda row: sentence2vec(row), axis=1)
    feat['first_word_same'] = data.apply(lambda row: first_word_same(row), axis=1)
    feat['len_diff'] = data.apply(lambda row: difference_in_length(row), axis=1)
    feat['jaccard'] = data.apply(lambda row: jaccard_sim(row), axis=1)
    feat['cos'] = data.apply(lambda row: cosine(row), axis=1)

    print('done vec')

    if embedding:
        feat['wmd'] = data.apply(lambda row: wmd(row, lang, embedding), axis=1)
        feat['cos_gensim'] = data.apply(lambda row: cos_gensim(row, lang, embedding), axis=1)
    else:
        feat['wmd'] = data.apply(lambda row: wmd(row, lang), axis=1)
        feat['cos_gensim'] = data.apply(lambda row: cos_gensim(row, lang), axis=1)

    print('done emb')


    # feat['root_same'] = data.apply(lambda row: root_same(row, lang), axis=1)
    # feat['diff_pos_count'] = data.apply(lambda row: diff_pos_count(row), axis = 1)
    feat['tfidf_similarity'] = tfidf(data['def1_stop'], data['def2_stop'])

    print('done tfidf')

    for c_name in feats_to_scale:
        feat[c_name] = preprocessing.scale(feat[c_name])

    return feat


