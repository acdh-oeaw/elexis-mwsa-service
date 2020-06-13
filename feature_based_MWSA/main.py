import load, embeddings, nlp_pipelines, extract_features
from train_models import train_models_sklearn, get_predictions_for_testset
from endpoint import classify

train_folder = '/Users/lenka/Desktop/train'
languages = ['basque','bulgarian','estonian',
             'hungarian','italian','irish','portuguese',
             'russian','serbian','slovene','danish','dutch']


languages = ['basque']


trained_models = {}
balanced_data = {}
embed = {}
pipelines = nlp_pipelines.get_nlp_pipelines(languages)
features = {}
labels = {}



#initialize models

for lang in languages:
    print('loading ', lang)
    balanced_data[lang] = load.load_and_preprocess(lang, 'undersampling')
    print('loaded ', len(balanced_data[lang]))
    embed[lang] = embeddings.make_word_embedding(balanced_data[lang], lang)
    print('finished', lang)
    features[lang] = extract_features.extract_features(balanced_data[lang],[], lang)
    labels[lang] = balanced_data[lang]['relation']
    print('extracted features for', lang)

    #print(features, labels)

    trained_models[lang] = train_models_sklearn(features[lang],
                                          labels[lang])


get_predictions_for_testset(features['basque'], labels['basque'], 'basque')

example_json = [
    {
        "def1": "konponketa eskatzen duen eragozpen edo zailtasun egoera",
        "def2": "mina edo atsekabea eragiten duen gertaera",
        "lang": "basque",
        "lemma": "arazo"
    }
]  # pos optional


print(classify(trained_models['basque'],example_json))