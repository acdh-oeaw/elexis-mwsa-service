import pickle
import pandas as pd
import logging
from swagger_server.models import ScoreInput, Scores

class FeatureExtractionService:
    def extract(self, definition_pair):
        return []

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AlignmentScoringService:
    def __init__(self, english_model=None):
        logger.info('loading english model')
        self.english_model = EnglishMwsaModelService() if not english_model else english_model
        logger.info('english model loaded')

    def score(self, score_input):
        df = pd.DataFrame(
            data={'word': [score_input.pair.headword], 'pos': [score_input.pair.pos], 'def1': [score_input.pair.def1],
                  'def2': [score_input.pair.def2]})

        return [self._highest_score(self.english_model.predict(df))]

    def _highest_score(self, prob):
        best = None

        for label_prob in prob:
            if not best or label_prob[1] > best[1]:
                best = label_prob

        return Scores(alignment=best[0], probability=best[1])


class EnglishMwsaModelService:

    def __init__(self):
        file = 'models/en.pkl'
        with open(file, 'rb') as model_file:
            self.model = pickle.load(model_file)

    def predict(self, input):
        logger.info('determining mwsa score')
        predicted = self.model.predict_proba(input)
        logger.info('mwsa score calculated')

        return zip(self.model.classes_, predicted[0])
