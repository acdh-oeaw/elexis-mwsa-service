
import stanfordnlp



lang_codes = {'basque':'eu','bulgarian':'bg','danish':'da','dutch':'nl','estonian':'et',
             'german':'de','hungarian':'hu','italian':'it','irish':'ga','portuguese':'pt',
             'russian':'ru','serbian':'sr','slovene':'sl'}

pipelines = {}

def get_nlp_pipelines(languages):

    for lang in languages:
        #stanfordnlp.download(lang_codes[lang])
        pipelines[lang] = stanfordnlp.Pipeline(lang = lang_codes[lang])

    return pipelines