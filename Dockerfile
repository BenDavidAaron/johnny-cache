FROM python:3.10
 
WORKDIR /opt

COPY requirements.txt /opt/requirements.txt
COPY app/ /opt/app/
COPY alembic.ini /opt/alembic.ini
COPY alembic/ /opt/alembic/

RUN pip install -r /opt/requirements.txt

ENV JOHNNY_CACHE_DATA_PATH=/opt/data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
