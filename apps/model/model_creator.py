from apps import engine, mongo, dataset
from sklearn import datasets
from apps.model.normalization import Normalization
import pickle, datetime


class ModelCreator:
    ID = '_id'
    MODEL_COLLECTION = 'model'

    def __init__(self, collection, label):
        # self.algorithm = algorithm
        self.collection = collection
        self.label = label
        # self.features = features
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.model = self.data_collection.find_one().sort('date', 1)
        self.normalizator = Normalization(collection)

    def load_features(self):
        self.features = self.data_collection.find({}, self.features).sort(self.ID, 1)

    def load_flag(self):
        self.labels = self.data_collection.find({}, {self.label: 1}).sort(self.ID, 1)

    def create_model(self, activation='relu', alpha=1e-5, hidden_layer_sizes=(5, 2)):
        self.classfier = engine.MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        self.load_features()
        self.load_flag()

        # temp_features = list(map(lambda x : list(map(lambda p : x[p], x)), self.features))
        # temp_labels = list(map(lambda x : x[self.label], self.labels))

        temp_features = self.normalizator.get_normalize_data(self.features)
        temp_labels = self.normalizator.get_normalize_data(self.labels)

        self.classfier.fit(temp_features, temp_labels)

        model = pickle._dumps(self.classfier)
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.data_collection.insert({'model' : model, 'date': datetime.datetime.now()})

    def load_model(self, id):
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.model = self.data_collection.find_one({'_id' : id()})

    def load_model_last_update(self):
        self.data_collection = dataset[self.MODEL_COLLECTION]
        self.model = self.data_collection.find_one({'_id': id()}).sort('date', -1)

    def classify(self, data):
        if(self.classfier is None):
            self.classfier = pickle.loads(self.model)
        data_res = self.normalizator.get_normalize_data(data)
        result = self.classfier.predict(data_res)
        result_json = {
            'data' : data,
            'result' : result
        }
        return result_json