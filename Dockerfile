FROM python:3.12

WORKDIR /parser

RUN apt-get update && apt-get install -y sqlite3 && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]