FROM joyzoursky/python-chromedriver:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install flask flask-sqlalchemy flask-wtf selenium requests python-dotenv webdriver-manager==3.8.6

WORKDIR /app

COPY . .

# Start app
CMD ["python", "run.py"]