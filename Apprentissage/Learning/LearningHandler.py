import http.client
import json

import tornado.web
import tornado.httpclient


import Apprentissage.DataStoring as ds
import Apprentissage.Learning.LearningConfiguration as conf

import Apprentissage.Learning.LearningData as ld
import Apprentissage.Learning.LearningMain as LearningMain
import Apprentissage.HelperConfig as HelperConfig
import Apprentissage.Graphics.Curve as curve
import NP6HelperHttp

from collections import OrderedDict
import HelperJson
import pandas

import Apprentissage.BusinessModel.ResponseModel as ResponseModel



LEARNING_HANDLER_ROUTE = "http://localhost:5000/learning"


class LearningHandler(tornado.web.RequestHandler):
    """description of class"""

    def initialize(self):
        self.dataX = None
        self.predictData = None


    def get(self, **param):
        try:
            if "id" in param:
                df = pandas.read_json('result_learning.txt')
                df2 = df.set_index(["id"])
                learning = df2.ix[int(param['id'])]
                self.write(learning.to_json())
            else:
                file = open('result_learning.txt','r')
                array = json.load(file)
                file.close()
                self.write(json.dumps(array))

        except Exception as e:
            self.set_status(http.client.INTERNAL_SERVER_ERROR)


    def post(self, **param):
        try:
            if not NP6HelperHttp.content_type(self.request.headers["Content-type"], "application/json"):
                self.set_status(http.client.UNSUPPORTED_MEDIA_TYPE,
                                "Expecting application/json")
            else:
                uri = self.request.uri
                data = learning_implementation(uri, self.request.body)

                #ecriture des résultats en format JSON.
                self._write_buffer = data["result"]
                self.predict = data["dataLearning"].predict

        except ValueError as e:
            print(e)
            self.set_status(http.client.BAD_REQUEST)
        except Exception as e:
            print(e)
            self.set_status(http.client.INTERNAL_SERVER_ERROR)

    def learning_implementation(uri, body):
        if  type(body) is not dict:
            bodyjson = body.decode()
        else :
            bodyjson = json.dumps(body,cls=HelperJson.HelperJson)
        c = json.loads(bodyjson, object_hook=conf.as_learning_configuration)
        myDataPrepa = ds.DataStoring()
        myDataPrepa.data = c.data
        myDataPrepa.predictData = c.predictData
        myDataLearning = ld.LearningData()
        #lancement du calcul

        LearningMain.LearningMain.choose_model(myDataPrepa, myDataLearning, uri)
                
        #ROC Curve corrige le probleme si preparation sur RedList (str) prends
        #les 1-2
        #myDataLearning=curve.Curve.curve_graphic(myDataLearning)
                
        # affichage des resultats obtenus
        model = uri.split('/', 2)
        whichModel = model[2]
        #recupère le différent paramètres et resultats de l'apprentissage
        data =  {"resultat" : 
                 ResponseModel.ResponseModel.data_learning_to_return_response_model(myDataLearning,whichModel),
                 "dataLearning" : myDataLearning}
        return data

    def put(self, **param):
        self.set_status(http.client.NOT_IMPLEMENTED)

    def delete(self, **param):
        self.set_status(http.client.NOT_IMPLEMENTED)
