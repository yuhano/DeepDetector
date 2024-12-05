from flask import Flask, render_template
from api.logs import logs_blueprint

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
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=4000)
