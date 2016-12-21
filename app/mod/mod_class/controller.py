from flask import Blueprint, jsonify
from flask.globals import request

from app import auth
from app.model.model_creator import ModelCreator
from app.model.normalization import Normalization

# Define the blueprint
mod_class = Blueprint('machine', __name__, url_prefix='/machine')
COLLECTION_NAME = 'ips_dataset'
LABEL_FIELD = {'Label':1, '_id' : 0}
FEATURES_LIST = {'﻿Date': 1, 'flow start': 1, 'Durat': 1, 'Prot': 1, 'Src IP Addr': 1, 'Src Port': 1, 'Dst IP Addr': 1,
                 'Dst Port': 1, 'Flags': 1, 'Tos': 1, 'Packets': 1, 'Bytes': 1, 'Flows': 1, '_id':0}

@mod_class.route('/prior-knowledge', methods=['GET', 'POST'])
# @auth.login_required
def normalization():
    normalizator = Normalization(COLLECTION_NAME)
    normalizator.drop_prior_knowledge()
    normalizator.generate_normalizaiton()
    return jsonify(message='normalization done :)')


# Set the route and accepted methods
@mod_class.route('/train', methods=['GET', 'POST'])
# @auth.login_required
def training():
    model_creator = ModelCreator(COLLECTION_NAME, FEATURES_LIST, LABEL_FIELD)
    model_creator.create_model()
    return jsonify(message='training done :)')


@mod_class.route('/classification', methods=['POST'])
@auth.login_required
def classify():
    content = request.json
    model_creator = ModelCreator(COLLECTION_NAME, LABEL_FIELD)
    result = model_creator.classify(content)
    return jsonify(result)
