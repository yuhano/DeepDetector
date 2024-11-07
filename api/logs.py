from flask import Blueprint, jsonify

logs_blueprint = Blueprint('logs', __name__)

@logs_blueprint.route('/', methods=['GET'])
def logs():
    return jsonify({'message': 'Logs retrieved'})