import os

from sklearn import metrics
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
import scipy
import numpy as np
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn import neighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn import svm

from sklearn.model_selection import cross_validate,KFold



import pandas as pd

global files

features_directory = r'D:\BotDetection-master\BotDetection-master\data\features'


def get_data_from_folders(data_folders):
    data = None
    classifications = []

    for folder in data_folders:
        # Retrieve key and mouse features for a single user
        key_data = pd.read_csv(os.path.join(features_directory, folder, 'key.csv'))
        mouse_data = pd.read_csv(os.path.join(features_directory, folder, 'mouse.csv'))
        # Combine key and mouse features from the user into one row
        merged_data = pd.concat([key_data, mouse_data], axis=1)
        # Determine classification of user from folder name and add to classifications
        classification = 'human' if 'human' in folder else 'bot'
        classifications.append(classification)
        # Merge feature row with existing data set
        data = merged_data if data is None else pd.concat([data, merged_data], ignore_index=True)

    return data, classifications
def get_data_for_advanced_bot():
    global files
    # Retrieve all folders from features directory. Each user's data is in a separate folder.
    folders = [f for f in os.listdir(features_directory) if os.path.isdir(os.path.join(features_directory, f))]

    human_folders = [f for f in folders if 'human' in f]
    advanced_bot_folders = [f for f in folders if 'advanced' in f]

    data_folders = human_folders + advanced_bot_folders
    return get_data_from_folders(data_folders)


def get_data_for_simple_bot():
    global files
    # Retrieve all folders from features directory. Each user's data is in a separate folder.
    folders = [f for f in os.listdir(features_directory) if os.path.isdir(os.path.join(features_directory, f))]

    human_folders = [f for f in folders if 'human' in f]
    simple_bot_folders = [f for f in folders if 'simple' in f]

    data_folders = human_folders + simple_bot_folders
    return get_data_from_folders(data_folders)
#get_data_for_simple_bot()

def print_results(results):
    # Print accuracy, precision, recall, and F1 score results from a classifier
    # The mean() is there because cross validation evaluates on each 'split' of data, so the
    # number of results is the same as the number of splits.
    print('Accuracy: {:0.2f}%'.format(results['test_accuracy'].mean() * 100))
    print('Precision: {:0.2f}%'.format(results['test_precision'].mean() * 100))
    print('Recall: {:0.2f}%'.format(results['test_recall'].mean() * 100))
    print('F1 score: {:0.2f}%'.format(results['test_f1_score'].mean() * 100))
    print('\n')

def main():
    # This contains the human and simple bot data
    X_simple, y_simple = get_data_for_simple_bot()

    # This contains the human and advanced bot data
    X_advanced, y_advanced = get_data_for_advanced_bot()
    classifiers = []
    cv = KFold(n_splits=2, shuffle=True)
    rfc = RandomForestClassifier()
    dt = DecisionTreeClassifier()
    SVM = svm.SVC(kernel = 'linear')
    knn = neighbors.KNeighborsClassifier(n_neighbors=3, weights = 'uniform')
    classifiers.append(knn)
    classifiers.append(rfc)
    classifiers.append(dt)
    classifiers.append(SVM)
    #knn.fit(X_simple, y_simple)
    #knn.fit(X_advanced,y_simple)
    #prediction = knn.predict()

    scoring = {'accuracy': make_scorer(accuracy_score),
               'precision': make_scorer(precision_score, pos_label='bot'),
               'recall': make_scorer(recall_score, pos_label='bot'),
               'f1_score': make_scorer(f1_score, pos_label='bot')}

    for clf in classifiers:
        print('Results for classifier: {}'.format(str(clf)))
        print('=================================================\n')

        # Simple bot results (human + simple data)
        print('Simple Bot Results')
        print('------------------')
        results = cross_validate(clf, X_simple, y_simple, cv=cv, scoring=scoring)
        print_results(results)

        # This is commented out for now because there's not enough advanced bot data for this data.
        # Advanced bot results (human + advanced data)
        # print('Advanced Bot Results')
        # print('--------------------')
        # results = cross_validate(rfc, X_advanced, y_advanced, cv=cv, scoring=scoring)
        # print(results)


if __name__ == '__main__':
    main()
