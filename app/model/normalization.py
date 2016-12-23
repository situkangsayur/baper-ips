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

    def get_normalize_data(self, data, is_label, label):

        temp_feature = list(map(lambda x: x, dataset[self.collection].find_one({}, {self.field_label:0,'_id': 0})))
        if is_label:
            temp_feature = label

        def search_value(temp):
            if(len(temp) == 13):
                print(temp)
                print(len(temp))
            else:
                if(is_label):
                    print('label : ')
                    print(temp)
                else:
                    print('less or more than 13')

            temp_array = [];

            if(is_label==False):

                for temp_field in temp_feature:
                    temp_values = dataset[self.COLLECTION_NAME].find_one({'field': temp_field}, {'_id': 0})
                    temp_value = list(filter(lambda x: str(x['value']) == str(temp[temp_field]), temp_values['values']))
                    temp_array.append(temp_value[0]['norm'])

                print(temp_array)
                return temp_array
            else:
                temp_values = dataset[self.COLLECTION_NAME].find_one({'field': temp_feature}, {'_id': 0})

                temp_value = list(filter(lambda x: str(x['value']) == str(temp[temp_feature]), temp_values['values']))
                #     print(p)
                temp_array.append(temp_value[0]['id'])
                print(temp_array)
                return temp_array

        return list(map(search_value, data))

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

            print(temp)
            print(min(range_val))
            print(max(range_val))
            tupple = list(
                map(lambda x, y: {'id': x, 'value': y, 'norm': self.normal_value(x, min(range_val), max(range_val))}, range_val,
                    temp_knowledge))

            prior_knowledge['_id'] = uuid.uuid1()
            prior_knowledge['field'] = temp
            prior_knowledge['values'] = tupple

            dataset[self.COLLECTION_NAME].insert(prior_knowledge)
