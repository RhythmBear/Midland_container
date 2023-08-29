FROM ubuntu:latest

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN sudo dpkg -i google-chrome-stable_current_amd64.deb

RUN pip3 install --upgrade pip

RUN pip3 install flask flask-sqlalchemy flask-wtf selenium requests python-dotenv webdriver-manager==3.8.6

WORKDIR /app

COPY . .

# Start app
CMD ["python", "run.py"]