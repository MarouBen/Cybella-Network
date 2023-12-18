FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /networkDocker

ADD . /networkDocker/

COPY requirements.txt /networkDocker/

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

COPY . /networkDocker/

EXPOSE 8000

CMD ["python3", "manage.py", "runserver","0.0.0.0:8000"]