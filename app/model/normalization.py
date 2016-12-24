import uuid
from app import engine, dataset
import pickle, datetime


class Normalization():
    ID = '_id'
    COLLECTION_NAME = 'prior_knowledge'

    def __init__(self, collection_ref, field_label):
        self.collection = collection_ref
        self.field_label = field_label

    def load_dataset(self):
        self.dataset = dataset[self.collection].find({}, {'_id': 0}).sort(self.ID, -1)

    def drop_prior_knowledge(self):
        dataset[self.COLLECTION_NAME].drop()

    def normal_value(self, value, min, max):
        if(max == 0):
            return 0
        else:
            return (max - value) / (max - min)

    def get_normalize_single_data(self, data):
        temp_array = []

        for temp_field in data:
            print(temp_field)
            temp_values = dataset[self.COLLECTION_NAME].find_one({'field': temp_field}, {'_id': 0})
            temp_value = list(filter(lambda x: x['value'] == data[temp_field], temp_values['values']))
            temp_array.append(temp_value[0]['norm'])

        return temp_array

    def get_denormaliza_data(self, field_name, field_value):
        values = dataset[self.COLLECTION_NAME].find_one({'field' : field_name},{'_id':0})
        print(values)
        temp = [x for x in values['values'] if x['id'] == field_value]
        return temp[0]['value']

    def get_normalize_data(self, data, is_label, label):

        temp_feature = list(map(lambda x: x, dataset[self.collection].find_one({}, {self.field_label:0,'_id': 0})))
        if is_label:
            temp_feature = label

        def search_value(temp):

            temp_array = [];

            if(is_label==False):

                for temp_field in temp_feature:
                    temp_values = dataset[self.COLLECTION_NAME].find_one({'field': temp_field}, {'_id': 0})
                    temp_value = list(filter(lambda x: x['value'] == temp[temp_field], temp_values['values']))
                    temp_array.append(temp_value[0]['norm'])

                return temp_array
            else:
                temp_values = dataset[self.COLLECTION_NAME].find_one({'field': temp_feature}, {'_id': 0})
                temp_value = list(filter(lambda x: x['value'] == temp[temp_feature], temp_values['values']))
                temp_array.append(temp_value[0]['id'])

                return temp_array

        return list(map(search_value, data))

    def generate_normalizaiton(self):
        self.load_dataset()
        features = dataset[self.collection].find_one({}, {'_id': 0})
        temp_feature = list(map(lambda x: x, features))

        prior_knowledge = {};
        temp_dataset = list(dataset[self.collection].find({}, {'_id': 0}))
        for temp in temp_feature:

            temp_knowledge = list(set(map(lambda x: x[temp], temp_dataset)))
            range_val = list(range(0, len(temp_knowledge)))
            zipped = zip(range_val, temp_knowledge)

            tupple = list(
                map(lambda x, y: {'id': x, 'value': y, 'norm': self.normal_value(x, min(range_val), max(range_val))}, range_val,
                    temp_knowledge))

            prior_knowledge['_id'] = uuid.uuid1()
            prior_knowledge['field'] = temp
            prior_knowledge['values'] = tupple

            dataset[self.COLLECTION_NAME].insert(prior_knowledge)
