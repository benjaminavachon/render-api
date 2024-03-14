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

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]