from flask import Blueprint, jsonify
import json
from datetime import datetime

logs_blueprint = Blueprint('logs', __name__)

@logs_blueprint.route('/', methods=['GET'])
def logs():
    # log.json 파일에서 데이터 읽기
    try:
        with open('log.json', 'r', encoding='utf-8') as file:
            logs = json.load(file)
    except FileNotFoundError:
        return jsonify(error="log.json file not found"), 404
    except json.JSONDecodeError:
        return jsonify(error="Error decoding JSON"), 400

    # 로그 데이터를 JSON 형식으로 변환
    log_list = []
    for log in logs:
        log_entry = {
            'input_id': log.get('input_id'),
            'input_passwd': log.get('input_passwd'),
            'source_addr': log.get('source_addr'),
            'result': log.get('result') == 'true',  # 문자열을 boolean으로 변환
            'time': log.get('time')  # time은 문자열로 저장되어 있다고 가정
        }

        # time이 datetime 객체인 경우 ISO 8601 형식으로 변환
        if isinstance(log_entry['time'], str):
            try:
                log_entry['time'] = datetime.fromisoformat(log_entry['time']).isoformat()
            except ValueError:
                pass  # 변환 실패 시 원래 문자열 유지

        log_list.append(log_entry)

    return jsonify(logs=log_list)
