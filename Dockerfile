FROM python:3.10
 
WORKDIR /opt

COPY requirements.txt /opt/requirements.txt
COPY app/ /opt/app/
COPY run.sh /opt/

RUN pip install -r /opt/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
