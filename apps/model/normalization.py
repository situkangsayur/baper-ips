from apps import engine, mongo, dataset
from sklearn import datasets
import pickle, datetime

class Normalization():
    ID = '_id'
    COLLECTION_NAME = 'prior_knowledge'

    def __init__(self, collection_ref):
        self.collection = collection_ref


    def load_dataset(self):
        self.dataset = dataset[self.collection].find().sort(self.ID, 1)


    def normal_value(self, value, min, max):
        return (max - value)/(max-min)

    def get_normalize_data(self,data):
        temp_feature = list(map(lambda  x: x, data))
        temp_feature

    def generate_normalizaiton(self):
        self.load_dataset()
        features = dataset[self.collection].find_one();
        temp_feature = list(map(lambda x: x, features))

        prior_knowledge = {};
        # def add_prio_knowledge(x,i) :
        #     data['id']
        for temp in temp_feature:

            temp_knowledge = list(map( lambda x: x[temp], self.dataset))
            range_val = list(range(0, len(temp_knowledge)))

            tupple = list(map(lambda x,y : (x,y,self.normal_value(x,0, len(temp_knowledge))), range_val))

            prior_knowledge[temp] = tupple

            dataset[self.COLLECTION_NAME].insert(prior_knowledge)
