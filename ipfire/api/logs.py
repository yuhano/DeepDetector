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
            "no": log.get('no'),                        # 패킷이 기록된 순서를 나타내는 번호
            "input_id": log.get('input_id'),            # HTTP 패킷에서 추출한 ID
            "input_passwd": log.get('input_passwd'),    # HTTP 패킷에서 추출한 PW
            "source_addr": log.get('source_addr'),
            "result": log.get('result'),                # RESULT는 FALSE 또는 TRUE로 설정
            "protocol": log.get('protocol'),            # PROTOCOL에 프로토콜 이름을 저장
            "src_port": log.get('src_port'),
            "dst_port": log.get('dst_port'),
            "time": log.get('time')
        }

        # time이 datetime 객체인 경우 ISO 8601 형식으로 변환
        if isinstance(log_entry['time'], str):
            try:
                log_entry['time'] = datetime.fromisoformat(log_entry['time']).isoformat()
            except ValueError:
                pass  # 변환 실패 시 원래 문자열 유지

        log_list.append(log_entry)

    return jsonify(log_list)


def add_log(log_entry):
    try:
        db = TinyDB('./api/db.json')
        log_table = db.table('log')
        log_table.insert(log_entry)  # 로그 데이터를 TinyDB에 저장
    except Exception as e:
        print(f'Error: {e}')
        return