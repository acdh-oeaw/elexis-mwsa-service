import logging
import pickle

import pandas as pd

from swagger_server.models import Scores

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FeatureExtractionService:
    def extract(self, definition_pair):
        return []


class AlignmentScoringService:
    def __init__(self, lang_model=None):
        logger.info('loading english model')
        self.model = ModelService() if not lang_model else lang_model
        logger.info('english model loaded')

    def score(self, score_input):
        df = pd.DataFrame(
            data={'word': [score_input.pair.headword], 'pos': [score_input.pair.pos], 'def1': [score_input.pair.def1],
                  'def2': [score_input.pair.def2]})

        return [self._highest_score(self.model.predict(score_input.pair.lang, df))]

    def _highest_score(self, prob):
        best = None

        for label_prob in prob:
            if not best or label_prob[1] > best[1]:
                best = label_prob

        return Scores(alignment=best[0], probability=best[1])


class ModelService:

    def __init__(self):
        self.model_map = {}

        en_file_path = 'models/en.pkl'
        de_file_path = 'models/de.pkl'

        with open(en_file_path, 'rb') as en_file:
            self.model_map['en'] = pickle.load(en_file)

        with open(de_file_path, 'rb') as de_file:
            self.model_map['de'] = pickle.load(de_file)

    def predict(self, lang, input):
        logger.info('determining mwsa score')
        predicted = self.model_map[lang].predict_proba(input)
        logger.info('mwsa score calculated')

        return zip(self.model_map[lang].classes_, predicted[0])
