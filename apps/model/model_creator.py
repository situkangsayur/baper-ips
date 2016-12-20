from apps import engine, mongo, dataset
from sklearn import datasets
import pickle, datetime


class ModelCreator:
    ID = '_id'
    MODEL_COLLECTION = 'model'

    def __init__(self, algorithm, collection, features, label):
        self.algorithm = algorithm
        self.collection = collection
        self.label = label
        self.features = features
        self.model_collection = dataset[self.MODEL_COLLECTION]
        self.model = self.model_collection.find

    def load_features(self):
        self.features = dataset.isp_dataset.find({}, self.features).sort(self.ID, 1)

    def load_flag(self):
        self.labels = dataset.isp - dataset.find({}, {self.label: 1}).sort(self.ID, 1)

    def create_model(self, activation='relu', alpha=1e-5, hidden_layer_sizes=(5, 2)):
        self.result = engine.MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        self.load_features()
        self.load_flag()

        temp_features = list(map(lambda x : list(map(lambda p : x[p], x)), self.features))
        temp_labels = list(map(lambda x : x[self.label], self.labels))

        self.result.fit(temp_features, temp_labels)

        model = pickle._dumps(self.result)
        self.model_collection = dataset[self.MODEL_COLLECTION]
        self.model_collection.insert({'model' : model, 'date': datetime.datetime.now()})

    def load_model(self, id):
        self.model_collection = dataset[self.MODEL_COLLECTION]
        self.model = self.model_collection.find_one({'_id' : id()})

    def classify(self, data):
        temp_model = pickle.loads(self.model)
        result = temp_model.predict(data)
        data = {
            'data' : data,
            'result' : result
        }
        return data