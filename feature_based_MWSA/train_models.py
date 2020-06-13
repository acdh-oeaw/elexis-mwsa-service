import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from pprint import pprint
from load import load_test_set

def train_and_test(data, with_testset=False):

    trained_models = train_models_sklearn(data['pd']['x_trainset'],
                                          data['pd']['y_trainset'])

    cross_val_models(trained_models, data['pd']['x_trainset'],
                     data['pd']['y_trainset'])

    if with_testset:
        return compare_on_testset(trained_models, data['pd']['x_testset'])


def compare_on_testset(trained_models, test_set):
    predictions = []
    for model in trained_models:
        # print(test_set.mean())
        test_set = test_set.replace([np.inf, -np.inf], np.nan)
        clean = test_set.fillna(test_set.mean())
        predict = model.predict(clean)

        results = model.predict_proba(clean)

        predictions.append((predict, results))

    return predictions


def cross_val_models(models, x_train, y_train):
    for estimator in models:
        run_cv_with_dataset(estimator, x_train, y_train)


def run_cv_with_dataset(model, trainset, y_train):
    trainset = trainset.replace([np.inf, -np.inf], np.nan)
    trainset = trainset.fillna(trainset.mean())

    scores = cross_val_score(model, trainset, y_train, cv=5)
    print('Cross validation scores for model' + model.__class__.__name__ + '\n')
    print("Accuracy: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2) + '\n')


def train_models_sklearn(x_train, y_train):
    # todo: add optional choice of classifier and params as json

    lr = {'estimator': LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=500), 'parameters': {}}
    svm_model = {
        'estimator': SVC(),
        'parameters': {
            'C': [3, 5, 10],
            'kernel': ['rbf', 'linear', 'poly', 'sigmoid']
        }
    }
    rf = {
        'estimator': RandomForestClassifier(),
        'parameters': {
            'bootstrap': [True],
            'max_depth': [5, 10],  # 2 3 7
            'max_features': [2, 3],
            'min_samples_leaf': [3, 5],  # 4
            'min_samples_split': [2, 5, 10],  # 8 12
            'n_estimators': [50, 100]  # 200
        }
    }
    dt = {'estimator': DecisionTreeClassifier(), 'parameters': {}}

    models = {'unscaled': [lr]}

    tuned_models = tune_hyperparams(models, x_train, y_train)

    return tuned_models


def tune_hyperparams(estimators, x_train, y_train):
    result = []
    for estimator in estimators['unscaled']:
        params = estimator['parameters']

        scores = ['f1'] #,'precision', 'recall']

        for score in scores:
            print("# Tuning hyper-parameters for %s" % score)
            print()

            grid_search = GridSearchCV(estimator=estimator['estimator'], param_grid=params,
                                       scoring='%s_weighted' % score, cv=5,
                                       n_jobs=-1, verbose=1)

            print("Performing grid search...")
            print("parameters:")
            pprint(params)

            x_train = x_train.replace([np.inf, -np.inf], np.nan)
            x_train = x_train.fillna(x_train.mean())

            grid_search.fit(x_train, y_train)
            print()

            means = grid_search.cv_results_['mean_test_score']
            stds = grid_search.cv_results_['std_test_score']
            print('Precision: \n')
            # for mean, std, parameters in zip(means, stds, grid_search.cv_results_['params']):
            #    print("%0.3f (+/-%0.03f) for %r"
            #                      % (mean, std * 2, parameters) + '\n')

            print("Best score: %0.3f" % grid_search.best_score_ + '\n')
            print("Best parameters set:\n")
            best_parameters = grid_search.best_estimator_.get_params()
            for param_name in sorted(params.keys()):
                print("\t%s: %r" % (param_name, best_parameters[param_name]) + '\n')

            result.append(grid_search.best_estimator_)

    return result


def get_predictions_for_testset(features, labels, lang):
    data = {'pd': {}}
    data['pd']['x_trainset'] = features
    data['pd']['y_trainset'] = labels

    test_features = load_test_set(lang)
    data['pd']['x_testset'] = test_features

    predictions = train_and_test(data, with_testset=True)

    for predict in predictions:
        print('pred ', len(predict[0]))
        print('prob ', len(predict[1]))

def print_predictions(test_data, predictions, lang, ind=''):
    test_data = test_data.drop(['def1_clean', 'def2_clean', 'def1_stop', 'def2_stop'], axis=1)
    test_data['prediction'] = predictions
    test_data.to_csv(lang + ind + ".csv", sep="\t", encoding='utf-8', index=False, header=False)

