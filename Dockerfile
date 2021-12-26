FROM python:3.8

ENV IS_DOCKER=true

ARG CHROME_VER="96.0.4664.110-1"
ARG CHROME_DRIVER_VER="96.0.4664.45"

# add trusted keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# add Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# install chrome and unzip
RUN apt-get -y update && apt-get install -y \
    google-chrome-stable=${CHROME_VER} \
    unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VER}/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver_linux64.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

WORKDIR /app

# install python reqs
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]
CMD ["src/run.py"]