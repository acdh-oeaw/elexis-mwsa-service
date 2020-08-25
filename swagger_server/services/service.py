import pickle
import pandas as pd

from swagger_server.models import ScoreInput, Scores


class FeatureExtractionService:
    def extract(self, definition_pair):
        return []


class AlignmentScoringService:
    def score(self, score_input):
        df = pd.DataFrame(
            data={'word': [score_input.pair.headword], 'pos': [score_input.pair.pos], 'def1': [score_input.pair.def1],
                  'def2': [score_input.pair.def2]})
        file = 'models/en.pkl'
        with open(file, 'rb') as model_file:
            model = pickle.load(model_file)
            predicted = model.predict_proba(df)
            zipped = zip(model.classes_, predicted[0])

        return self._highest_score(zipped)

    def _highest_score(self, prob):
        best = None
        for label_prob in prob:
            if not best or label_prob[1] > best[1]:
                best = label_prob

        return Scores(alignment=best[0], probability=best[1])
