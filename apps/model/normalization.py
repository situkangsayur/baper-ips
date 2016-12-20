from apps import engine, mongo, dataset
from sklearn import datasets
import pickle, datetime

class Normalization():

    def __init__(self, collection_ref):
        self.collection = collection_ref


    def load_dataset(self):
        self.dataset = dataset.isp_dataset.find().sort(self.ID, 1)

    def generate_normalizaiton(self):

