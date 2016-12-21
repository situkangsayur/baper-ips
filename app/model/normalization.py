import uuid
from app import engine, dataset
import pickle, datetime


class Normalization():
    ID = '_id'
    COLLECTION_NAME = 'prior_knowledge'

    def __init__(self, collection_ref):
        self.collection = collection_ref

    def load_dataset(self):
        self.dataset = dataset[self.collection].find({}, {'_id': 0}).sort(self.ID, 1)

    def drop_prior_knowledge(self):
        dataset[self.COLLECTION_NAME].drop()

    def normal_value(self, value, min, max):
        return (max - value) / (max - min)

    def get_normalize_data(self, data):

        temp_feature = list(map(lambda x: list(map(lambda p: p, x)), data))
        temp_values = list(map(lambda x: list(map(lambda p: x[p], x)), data))
        # temp_zip = zip(temp_feature, temp_values)
        print('data : ')
        print(list(temp_feature))
        print(list(temp_values))

        def search_value(field, value):
            temp_values = list(dataset[self.COLLECTION_NAME].find_one({'field': field}, {'_id': 0}))
            temp_value = filter(lambda x: x.value == value, temp_values.values)
            value = 0
            if (temp_value[0] is None):
                value = temp_value[0]
            return value

        return list(map(search_value, temp_feature, temp_values))

    def generate_normalizaiton(self):
        self.load_dataset()
        features = dataset[self.collection].find_one({}, {'_id': 0})
        # print('val' + features)
        temp_feature = list(map(lambda x: x, features))

        # for t in temp_feature:
        #     print(t)
        prior_knowledge = {};
        # def add_prio_knowledge(x,i) :
        #     data['id']
        temp_dataset = list(dataset[self.collection].find({}, {'_id': 0}))
        for temp in temp_feature:

            temp_knowledge = list(set(map(lambda x: x[temp], temp_dataset)))
            range_val = list(range(0, len(temp_knowledge)))

            zipped = zip(range_val, temp_knowledge)
            # print('zipp count :  ' + len(zipped))
            # for temp in zipped:
            #     print(temp)

            tupple = list(
                map(lambda x, y: {'id': x, 'value': y, 'norm': self.normal_value(x, 0, len(temp_knowledge))}, range_val,
                    temp_knowledge))

            prior_knowledge['_id'] = uuid.uuid1()
            prior_knowledge['field'] = temp
            prior_knowledge['values'] = tupple

            dataset[self.COLLECTION_NAME].insert(prior_knowledge)
