from gensim.models import Word2Vec
embeddings = {}

def make_word_embedding(dataset, lang):
    all_definitions = []
    for index, row in dataset.iterrows():
        def1 = row['def1_tokenized'].replace('[', '').replace(']', '').replace('\'', '').split(',')
        def2 = row['def2_tokenized'].replace('[', '').replace(']', '').replace('\'', '').split(',')


        all_definitions.append((def1)) # with or without stopwords?
        all_definitions.append((def2))

    model = Word2Vec(all_definitions,
                     min_count=1,
                     size=200,
                     workers=2,
                     window=5,
                     iter=30)
    embeddings[lang] = model
    return model




