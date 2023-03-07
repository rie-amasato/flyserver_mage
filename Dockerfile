FROM python:3.9.2

COPY requirements.txt /root/ 
RUN pip install Flask
RUN pip install -r /root/requirements.txt

RUN mkdir source
COPY source/ /root/source/

WORKDIR /root/source/

CMD ["flask", "run", "--port=80", "--host=0.0.0.0"]
