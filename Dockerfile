FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY main.py ./
COPY models.py ./

EXPOSE 8080
CMD python main.py
