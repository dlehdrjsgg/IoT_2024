# Python 3.8을 기반 이미지로 사용
FROM python:3.9-bullseye

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN pip3 install flask flask_cors

# 애플리케이션 파일 복사
COPY app.py .
COPY items.json .

# 컨테이너가 시작될 때 실행할 명령
CMD ["python", "app.py"]