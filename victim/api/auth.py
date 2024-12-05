from flask import Blueprint, jsonify, request, Response
from tinydb import TinyDB
from datetime import datetime

auth_blueprint = Blueprint('auth', __name__)

# SQL 인젝션 공격 대상 될 수 있는 취약한 로그인 시스템 구현
@auth_blueprint.route('/', methods=['POST'])
def auth():
    data = request.get_json()
    user_id = data.get('id')
    user_passwd = data.get('passwd')

    # 입력값 검증
    if not user_id or not user_passwd:
        return jsonify({'error': 'Missing required fields: id or passwd'}), 400
    

    # 로그 데이터 콘솔에 출력
    log_entry = {
        'input_id': user_id,
        'input_passwd': user_passwd,
        'source_addr': request.remote_addr,
        'time': datetime.now().isoformat()  # 현재 시간을 ISO 형식으로 저장
    }

    try:
        # TinyDB 인스턴스 생성 및 db.json 파일 로드
        db = TinyDB('./api/db.json')
        log_table = db.table('log')
        log_table.insert(log_entry)  # 로그 데이터를 TinyDB에 저장
    except Exception as e:
        print(f'Error saving log: {e}')
        return jsonify({'error': 'Failed to process request due to server error'}), 500

    return jsonify({'message': 'Login successful'}), 200

