from sklearn.externals.six import StringIO
import time 
from sklearn import ensemble
from sklearn.externals import joblib
from sklearn.metrics import roc_curve, auc
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
import matplotlib.pyplot as plt
from scipy.stats import randint as sp_randint
import Apprentissage.HelperConfig as HelperConfig
import Apprentissage.Sample.LaunchFit as LaunchFit
import Apprentissage.Sample.Preparation as Preparation
import Apprentissage.Graphics.Curve as Curve
import Apprentissage.Graphics.FinalModel as FinalModel
import configparser
import os
import NP6HelperConfig
import pickle

class RandomForest(object):

    def grid_search_parameters():
        return [{'criterion': ['gini','entropy'], \
                            'max_depth': [10,20,30,40,50,60],\
                            'min_samples_leaf': [20, 200, 1000],  # normalement c'est entre 2et 10 % du nombre de ligne dans l'echantillon
                            'n_estimators': [5, 10, 15, 20]}]

    def randomized_search_parameters():
        return {'criterion': ['gini','entropy'], \
                            'max_depth': sp_randint(10, 60),\
                            'min_samples_leaf':sp_randint(200, 1000), \
                            'n_estimators' :sp_randint(5, 20)}

    def exec(dataEl, dataLearning):
        
        config = NP6HelperConfig.get_config(__file__)
        tps1 = time.clock() 
        dataLearning = Preparation.Preparation.split_sample(dataEl, dataLearning)

        tunedParameters = RandomForest.randomized_search_parameters()

        score = 'f1'
     #   clf = GridSearchCV(ensemble.RandomForestClassifier(), tuned_parameters,cv=5, scoring=score)

        clf = RandomizedSearchCV(ensemble.RandomForestClassifier(), param_distributions=tunedParameters, \
            n_iter=int(config['Apprentissage']['iter']), cv=5, scoring=score)
        finalclf = LaunchFit.LaunchFit.execute_fit(clf, dataLearning)
        #on exporte l'arbre au format .dot, qui peut etre lu par le logiciel graphviz
        #tree.export_graphviz(f, out_file="test.dot")
        
        tps2 = time.clock() 
        temp = tps2-tps1
        print("TEMPS EXECUTION TOTAL : " + str(temp))
        dataLearning.executeTime=temp
        dataLearning.pkl=finalclf
        #on lance la prédiction sur les données initiales pour récupérer la valeur prédite utilisée pour la logistic regression
        dataLearning.predict=finalclf.predict(dataEl.data)
        return dataLearning