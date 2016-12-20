from flask import Blueprint, render_template, jsonify
from apps import auth

# Define the blueprint
mod_home = Blueprint('home', __name__, url_prefix='/')


# Set the route and accepted methods
@mod_home.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@mod_home.route('help', methods=['GET'])
@auth.login_required
def help():
    return jsonify(message='Can I help you?? :)')