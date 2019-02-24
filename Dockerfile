FROM ubuntu:16.04

MAINTAINER ddd7788989

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    pip install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

COPY ./app.py /app/app.py

COPY ./im2txt_inference.py /app/im2txt_inference.py

COPY chkpt /app/chkpt

COPY im2txt /app/im2txt

WORKDIR /app

RUN pip install -r requirements.txt

#COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
