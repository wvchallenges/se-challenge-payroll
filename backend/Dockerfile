FROM python:3.7.0-alpine

WORKDIR /app
COPY req.txt /app
RUN pip install -r req.txt
COPY . /app
RUN python db/db.py init
RUN python db/db.py migrate
CMD ["python","app.py"]
