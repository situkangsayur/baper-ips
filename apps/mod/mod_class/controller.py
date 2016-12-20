from flask import Blueprint, render_template, jsonify
from apps import auth

# Define the blueprint
mod_home = Blueprint('classify', __name__, url_prefix='/')


# Set the route and accepted methods
@mod_home.route('/train', methods=['GET', 'POST'])
@auth.login_required
def training():
    return render_template("index.html")


@mod_home.route('/classify', methods=['GET'])
@auth.login_required
def classify():
    return jsonify(message='Can I help you?? :)')