from flask import Blueprint, jsonify

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/', methods=['GET'])
def auth():
    return jsonify({'message': 'Authentication successful'})