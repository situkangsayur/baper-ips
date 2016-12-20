from flask import jsonify
from flask.blueprints import Blueprint
from flask.globals import request

from apps import auth
from apps.model.model_creator import ModelCreator
from apps.model.normalization import Normalization

# Define the blueprint
mod_class = Blueprint('classify', __name__, url_prefix='/classify')
COLLECTION_NAME = 'isp_dataset'
LABEL_FIELD = 'flag'


@mod_class.route('/prior-knowledge', methods=['GET', 'POST'])
@auth.login_required
def training():
    normalizator = Normalization(COLLECTION_NAME)
    normalizator.generate_normalizaiton()
    return jsonify(message='normalization done :)')


# Set the route and accepted methods
@mod_class.route('/train', methods=['GET', 'POST'])
@auth.login_required
def training():
    model_creator = ModelCreator(COLLECTION_NAME, LABEL_FIELD)
    model_creator.create_model()
    return jsonify(message='training done :)')


@mod_class.route('/classify', methods=['POST'])
@auth.login_required
def classify():
    content = request.json
    model_creator = ModelCreator(COLLECTION_NAME, LABEL_FIELD)
    result = model_creator.classify(content)
    return jsonify(result)