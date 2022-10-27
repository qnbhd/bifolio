FROM python:3.10

ENV PYTHONUNBUFFERED=1
WORKDIR /root

COPY cacher cacher

RUN pip install --upgrade pip
RUN pip install --user --no-cache-dir -r cacher/requirements.txt

ENV PYTHONPATH "$PWD:$PYTHONPATH"
CMD ["python3", "cacher/server.py", "run"]
