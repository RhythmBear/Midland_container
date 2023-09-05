FROM ubuntu:22.04

RUN apt-get update; apt-get clean

# Install wget.
RUN apt-get install -y wget

RUN apt-get install -y gnupg

# Set the Chrome repo.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Install Chrome.
RUN apt-get update && apt-get -y install google-chrome-stable

RUN apt-get -y install python3-pip

RUN pip3 install --upgrade pip

RUN pip3 install flask flask-sqlalchemy flask-wtf selenium requests python-dotenv webdriver-manager==3.8.6

WORKDIR /app

COPY . .

# Start app
CMD ["python3", "run.py"]
