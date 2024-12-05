from flask import Flask, render_template
from api.logs import logs_blueprint
import threading
from api.network_capture import start_packet_sniffing

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def dashboard():
        return render_template('dashboard.html')

    # API 블루프린트 등록
    app.register_blueprint(logs_blueprint, url_prefix='/api/logs')

    return app

if __name__ == '__main__':
    print("start")

    # 패킷 캡처를 위한 스레드 시작
    sniffing_thread = threading.Thread(target=start_packet_sniffing, daemon=True)
    sniffing_thread.start()

    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=4000)
