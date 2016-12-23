from app import engine, dataset
import numpy as np
from app.model.normalization import Normalization
import pickle, datetime


class ModelCreator:
    ID = '_id'
    MODEL_COLLECTION = 'model'

    def __init__(self, collection, features, labels, label_name):

        self.collection = dataset[collection]
        self.labels = labels
        self.label_name = label_name
        self.features = features
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.data_count = dataset[self.MODEL_COLLECTION].count()
        if(self.data_count > 0):
            self.model = self.data_collection.find({},{'_id' : 0}).sort("date", 1)[0]
            self.classfier = pickle.loads(self.model['model'])
        self.normalizator = Normalization(collection, label_name)

    def load_features(self):
        self.features = self.collection.find({}, self.features).sort(self.ID, -1)

    def load_flag(self):
        self.labels = self.collection.find({}, self.labels).sort(self.ID, -1)

    def create_model(self):
        self.classfier = engine.MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)

        self.load_features()
        self.load_flag()

        temp_list_features = list(self.features)
        temp_list_labels = list(self.labels)

        temp_features = self.normalizator.get_normalize_data(temp_list_features, False, '')
        temp_labels = self.normalizator.get_normalize_data(temp_list_labels, True, self.label_name)

        flatten = lambda l: [item for sublist in l for item in sublist]


        self.classfier.fit(temp_features, flatten(temp_labels))
        #
        model = pickle.dumps(self.classfier)
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.data_collection.insert({'model' : model, 'date': datetime.datetime.now()})

    def load_model(self, id):
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.model = self.data_collection.find_one({'_id' : id()},{'_id' : 0})

    def load_model_last_update(self):
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.model = self.data_collection.find_one({'_id': id()},{'_id' : 0}).sort('date', -1)

    def classify(self, data):
        if(self.model is None):
            self.model = self.data_collection.find({}, {'_id': 0}).sort("date", 1)[0]
            self.classfier = pickle.loads(self.model['model'])
        data_res = self.normalizator.get_normalize_single_data(data)
        result = self.classfier.predict(data_res)

        # result_json = {
        #     'data' : data,
        #     'result' : result
        # }
        print("--------------")
        print(result)
        return "ok"