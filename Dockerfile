FROM python:3.10

WORKDIR /auth

COPY ./requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir psycopg2 --upgrade -r requirements.txt

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN . env/bin/activate

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]