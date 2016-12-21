from app import engine, dataset
import numpy as np
from app.model.normalization import Normalization
import pickle, datetime


class ModelCreator:
    ID = '_id'
    MODEL_COLLECTION = 'model'

    def __init__(self, collection, features, label):
        # self.algorithm = algorithm
        # print('collection : ' + collection)
        self.collection = dataset[collection]
        self.label = label
        self.features = features
        self.data_collection = dataset[self.MODEL_COLLECTION]
        if(self.data_collection.count() > 0):
            self.model = self.data_collection.find({},{'_id' : 0}).sort("date", 1)[0]
        self.normalizatorFeature = Normalization(collection)
        self.normalizatorLabel = Normalization(collection)

    def load_features(self):
        self.features = self.collection.find({}, self.features).sort(self.ID, -1)

    def load_flag(self):
        self.labels = self.collection.find({}, self.label).sort(self.ID, -1)

    def create_model(self, activation='relu', alpha=1e-5, hidden_layer_sizes=(5, 2)):
        self.classfier = engine.MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        # self.classfier = svm.SVC()
        self.load_features()
        self.load_flag()

        temp_list_features = list(filter(lambda x: len(x)>0, self.features))
        # print('length : ' + temp_list_features.__len__())
        temp_list_labels = list(self.labels)

        # print(temp_features)
        temp_features = self.normalizatorFeature.get_normalize_data(temp_list_features, False, '')
        temp_labels = self.normalizatorLabel.get_normalize_data(temp_list_labels, True, 'label')

        self.classfier.fit(temp_features, temp_labels)
        #
        model = pickle._dumps(self.classfier)
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.data_collection.insert({'model' : model, 'date': datetime.datetime.now()})

    def load_model(self, id):
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.model = self.data_collection.find_one({'_id' : id()},{'_id' : 0})

    def load_model_last_update(self):
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.model = self.data_collection.find_one({'_id': id()},{'_id' : 0}).sort('date', -1)

    def classify(self, data):
        if(self.classfier is None):
            self.model = self.data_collection.find({}, {'_id': 0}).sort("date", 1)[0]
            self.classfier = pickle.loads(self.model)
        data_res = self.normalizator.get_normalize_data(data)
        result = self.classfier.predict(data_res)
        result_json = {
            'data' : data,
            'result' : result
        }
        return result_json