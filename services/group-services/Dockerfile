FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y git

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/mooover-org/mooover-corelib.git#egg=corelib

EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
