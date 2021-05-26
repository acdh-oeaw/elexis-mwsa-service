import logging
import pickle
import tensorflow as tf
import pandas as pd
from transformers import TFBertForSequenceClassification, BertTokenizerFast, PretrainedConfig

from swagger_server.exceptions.exceptions import LanguageNotSupportedException
from swagger_server.models import Scores, ScoreInput

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TransformerModel():
    def __init__(self, dir: str):
        self.model: TFBertForSequenceClassification = TFBertForSequenceClassification.from_pretrained(dir)
        self.config: PretrainedConfig = PretrainedConfig.from_pretrained(dir + '/config.json')
        self.tokenizer: BertTokenizerFast = BertTokenizerFast.from_pretrained(dir)


class FeatureExtractionService:
    def extract(self, definition_pair):
        return []


class TransformerService(object):
    def __init__(self):
        self.models = {}
        self.models['en'] = TransformerModel("models/mwsa_bert")
        self.models['de'] = TransformerModel("models/mwsa_bert_de")

    def predict(self, lang, input):
        if lang not in self.models.keys():
            raise LanguageNotSupportedException(lang)

        model: TransformerModel = self.models[lang]
        test_encodings = model.tokenizer([input.def1.values[0]], [input.def2.values[0]], truncation=True,
                                              padding='max_length', max_length=128, return_tensors="tf")
        logger.debug(test_encodings)

        tf_dataset: tf.data.Dataset = tf.data.Dataset.from_tensor_slices((
            dict(test_encodings)
        ))
        logger.info('determining mwsa score')

        predicted = model.model.predict(tf_dataset.batch(32))

        logger.info('mwsa score calculated {}'.format(predicted))
        logger.debug(list(model.config.id2label.values()))
        logger.debug(predicted[0])
        logger.debug(zip(model.config.id2label.keys(), predicted[0][0]))

        return zip(list(model.config.id2label.values()), predicted[0][0])


class AlignmentScoringService:
    def __init__(self, lang_model=None, transformer_model=None):
        logger.info('loading english model')
        self.model = ModelService() if not lang_model else lang_model
        self.transformer = TransformerService() if not transformer_model else transformer_model
        logger.info('english model loaded')

    def score(self, score_input: ScoreInput):
        df = pd.DataFrame(
            data={'word': [score_input.pair.headword], 'pos': [score_input.pair.pos], 'def1': [score_input.pair.def1],
                  'def2': [score_input.pair.def2]})

        if score_input.classifier == 'bert':
            return [self._highest_score(self.transformer.predict(score_input.pair.lang, df))]

        return [self._highest_score(self.model.predict(score_input.pair.lang, df))]

    def _highest_score(self, prob):
        best = None

        for label_prob in prob:
            logger.info('highest score')
            logger.info(label_prob)
            logger.info(best)
            if not best or label_prob[1] > best[1]:
                best = label_prob

        return Scores(alignment=best[0], probability=str(best[1]))


class ModelService:

    def __init__(self):
        self.model_map = {}
        self.pipeline_map = {}

        en_file_path = 'models/en.pkl'
        en_pipeline_path = 'models/pipeline/pipeline_english_nuig.tsv.pkl'
        de_file_path = 'models/de.pkl'
        de_pipeline_path = 'models/pipeline/pipeline_english_nuig.tsv.pkl'

        with open(en_pipeline_path, 'rb') as en_file:
            self.pipeline_map['en'] = pickle.load(en_file)

        with open(en_file_path, 'rb') as en_file:
            self.model_map['en'] = pickle.load(en_file)

        with open(de_file_path, 'rb') as de_file:
            self.model_map['de'] = pickle.load(de_file)

        with open(de_pipeline_path, 'rb') as de_file:
            self.pipeline_map['de'] = pickle.load(de_file)

    def predict(self, lang: str, input: pd.DataFrame):
        logger.info('determining mwsa score')
        try:
            features = self.pipeline_map[lang].transform(input)
        except KeyError:
            raise LanguageNotSupportedException(lang)

        predicted = self.model_map[lang].predict_proba(features)
        logger.info('mwsa score calculated')

        return zip(self.model_map[lang].classes_, predicted[0])
