FROM python:3.10

ENV PYTHONUNBUFFERED=1
WORKDIR /root

COPY bifolio bifolio

RUN pip install --upgrade pip
RUN pip install --user --no-cache-dir -r bifolio/requirements.txt

ENV PYTHONPATH "$PWD:$PYTHONPATH"
CMD ["python3", "bifolio/server.py", "run"]
