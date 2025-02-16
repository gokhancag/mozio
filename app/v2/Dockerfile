FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3 pip
RUN pip install flask
COPY hello.py /opt/
CMD FLASK_APP=/opt/hello.py flask run --host=0.0.0.0 --port=80
EXPOSE 80
