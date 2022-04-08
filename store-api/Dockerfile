FROM python:3.9.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY src .
ENV PYTHONPATH /usr/src/app

# Wait for database to load (in production the server should already be up)
CMD sleep 1 && uvicorn --host 0.0.0.0 storefront.main:app --log-level debug --use-colors

