FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
  google-chrome-stable=113.0.5672.92-1~deb11u1 \
  python3-pip

RUN pip3 install --upgrade pip

RUN pip3 install flask flask-sqlalchemy flask-wtf selenium requests python-dotenv webdriver-manager==3.8.6

WORKDIR /app

COPY . .

# Start app
CMD ["python", "run.py"]