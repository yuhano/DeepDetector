from flask import Blueprint

# 블루프린트 생성
api_bp = Blueprint('api', __name__)

# 엔드포인트 등록
from .logs import logs_blueprint

api_bp.register_blueprint(logs_blueprint, url_prefix='/logs')
