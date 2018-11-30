FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip3 install -r requirements.txt

RUN python3 manage.py collectstatic --noinput

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "pipetaxon.wsgi"]
