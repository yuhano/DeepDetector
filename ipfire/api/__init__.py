from flask import Blueprint

# 블루프린트 생성
api_bp = Blueprint('api', __name__)

# 엔드포인트 등록
from .logs import logs_blueprint
from .send_firewall import send_firewall_rule

api_bp.register_blueprint(logs_blueprint, url_prefix='/logs')
api_bp.register_blueprint(send_firewall_rule, url_prefix='/send_firewall')
