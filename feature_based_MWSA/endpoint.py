import pandas as pd
import numpy as np
from preprocessing import clean_punctuation, clean_stopwords, tokenize
from extract_features import extract_features



o = ['none', 'exact', 'broader', 'narrower', 'related']  # order of probabilities?


def classify(model, dic):
    # dic = json.loads(example_json)
    print(dic[0]["def1"])

    # trained classifiers should be objects which are initialized, for now a global var dictionary


    df = pd.DataFrame(dic)

    tokenized = tokenize(df, dic[0]['lang'])
    clean_def = clean_punctuation(tokenized)
    clean_def = clean_stopwords(clean_def, dic[0]['lang'])
    featureset = extract_features(clean_def, [], dic[0]['lang'])
    # print(featureset)

    # fix weird values from word2vec when definitions contain words which are not in the embedding
    test_set = featureset.replace([np.inf, -np.inf], np.nan)
    clean = test_set.fillna(test_set.mean())

    output = {}
    output['rfc'] = []
    output['rfc'].append({
        'prediction': model[0].predict(clean)[0],
        'probability': str(model[0].predict_proba(clean)[0].max())
    })

    return (output)


# skos: https://www.w3.org/TR/skos-reference/




