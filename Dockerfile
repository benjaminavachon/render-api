FROM ubuntu

WORKDIR /app

# install system dependencies
RUN apt-get update
# install dependencies
RUN apt install python3-pip -y
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

RUN apt-get install -y firefox

RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]