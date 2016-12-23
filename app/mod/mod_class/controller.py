from flask import Blueprint, jsonify
from flask.globals import request

from app import auth
from app.model.model_creator import ModelCreator
from app.model.normalization import Normalization

# Define the blueprint
mod_class = Blueprint('machine', __name__, url_prefix='/machine')
COLLECTION_NAME = 'ips_dataset'
LABEL_FIELD_NAME = 'label'
LABEL_FIELD = {LABEL_FIELD_NAME:1, '_id' : 0}
FEATURES_LIST = {'date': 1, 'flow_start': 1, 'durat': 1, 'prot': 1, 'src_ip_addr': 1, 'src_port': 1, 'dst_ip_addr': 1,
                 'dst_port': 1, 'flags': 1, 'tos': 1, 'packets': 1, 'bytes': 1, 'flows': 1, '_id':0}

@mod_class.route('/prior-knowledge', methods=['GET', 'POST'])
# @auth.login_required
def normalization():
    normalizator = Normalization(COLLECTION_NAME, LABEL_FIELD_NAME)
    normalizator.drop_prior_knowledge()
    normalizator.generate_normalizaiton()
    return jsonify(message='normalization done :)')


# Set the route and accepted methods
@mod_class.route('/train', methods=['GET', 'POST'])
# @auth.login_required
def training():
    model_creator = ModelCreator(COLLECTION_NAME, FEATURES_LIST, LABEL_FIELD, LABEL_FIELD_NAME)
    model_creator.create_model()
    return jsonify(message='training done :)')


@mod_class.route('/classification', methods=['POST'])
@auth.login_required
def classify():
    content = request.json
    model_creator = ModelCreator(COLLECTION_NAME, LABEL_FIELD, LABEL_FIELD_NAME)
    result = model_creator.classify(content)
    return jsonify(result)
