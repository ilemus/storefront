FROM python:3.9.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY src .
ENV PYTHONPATH /usr/src/app

CMD ["uvicorn", "--host", "0.0.0.0", "storefront.main:app"]

