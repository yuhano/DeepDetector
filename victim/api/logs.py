from flask import Blueprint, jsonify
from datetime import datetime
from tinydb import TinyDB

logs_blueprint = Blueprint('logs', __name__)

@logs_blueprint.route('/', methods=['GET'])
def logs():
    log_list = []

    # TinyDB 인스턴스 생성 및 db.json 파일 로드
    db = TinyDB('./api/db.json')
    log_table = db.table('log')

    # 로그 데이터를 JSON 형식으로 변환
    for log in reversed(log_table.all()):
        log_entry = {
            'input_id': log.get('input_id'),
            'input_passwd': log.get('input_passwd'),
            'source_addr': log.get('source_addr'),
            'result': log.get('result'),
            'time': log.get('time')  # time은 문자열로 저장되어 있다고 가정
        }

        # time이 datetime 객체인 경우 ISO 8601 형식으로 변환
        if isinstance(log_entry['time'], str):
            try:
                log_entry['time'] = datetime.fromisoformat(log_entry['time']).isoformat()
            except ValueError:
                pass  # 변환 실패 시 원래 문자열 유지

        log_list.append(log_entry)

    return jsonify(log_list)
