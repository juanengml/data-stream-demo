FROM python:3.7-buster


ENV TZ="America/Sao_Paulo"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update 
RUN apt upgrade --yes 
RUN pip install mysqlclient
RUN apt-get install python-mysqldb --yes

COPY requirementes.txt /consumer/requirementes.txt
COPY * /consumer/
WORKDIR /consumer
RUN  pip3 install -r requirementes.txt

CMD python3.7 ./consumer.py
