from flask import Blueprint, jsonify , request
import sqlite3
import json
from datetime import datetime

auth_blueprint = Blueprint('auth', __name__)
#sql 인젝션 공격 대상 될 수 있는 취약한 로그인 시스템 구현
@auth_blueprint.route('/', methods=['POST'])
def auth():
    data = request.get_json()
    user_id = data.get('id')
    user_passwd = data.get('passwd')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # SQL 인젝션 취약점이 있는 쿼리
    query = f"SELECT * FROM users WHERE id='{user_id}' AND passwd='{user_passwd}';"
    cursor.execute(query)
    user = cursor.fetchone()
   # 사용자 정보 콘솔에 출력
    if user:
        print("User found:", user)
        # 로그인 성공 시 사용자 정보를 반환
        response = {
            'result': 'true',
            'user_id': user[0],  # 예: 사용자 ID
            'message': 'Login successful'
        }
    else:
        print("User not found")
        response = {
            'result': 'false',
            'message': 'Invalid credentials'
        }

   # 로그 데이터 콘솔에 출력
    log_entry = {
        'input_id': user_id,
        'input_passwd': user_passwd,
        'source_addr': request.remote_addr,
        'result': response['result'],
        'time': datetime.now().isoformat()  # 현재 시간을 ISO 형식으로 저장
    }

    # 각 로그 항목 콘솔에 출력
    print("Log Entry:")
    for key, value in log_entry.items():
        print(f"{key}: {value}")

    return jsonify(response)