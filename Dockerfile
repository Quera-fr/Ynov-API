FROM continuumio/miniconda3

WORKDIR /home/app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY api.py .

COPY model.pkl .

CMD uvicorn api:app --port $PORT --host 0.0.0.0