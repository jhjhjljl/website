FROM python:3.13-slim AS build

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip3 install --no-cache-dir --requirement requirements.txt

COPY ./app /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--no-access-log" "--reload"]
