FROM python:3.14-alpine

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip3 install --no-cache-dir --requirement requirements.txt

COPY ./app /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
