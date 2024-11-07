# DeepDetector's Project

## Project Structure

```text
project/
├── app.py                      # Flask 앱의 진입점 파일
├── templates/                  # HTML 템플릿 폴더
│   ├── victim.html             # victim 페이지 템플릿
│   └── dashboard.html          # dashboard 페이지 템플릿
├── static/                     # 정적 파일 폴더 (CSS, JS 등)
│   ├── css/
│   └── js/
└── api/                        # API 관련 파일 폴더
    ├── __init__.py             # API 모듈 초기화 파일
    ├── auth.py                 # 인증 관련 API 엔드포인트
    └── logs.py                 # 로그 관련 API 엔드포인트
```

## 실행

1. python, flask 설치 되어 있는지 확인
2. 프로젝트 폴더에서 `python app.py` 명령어 실행
