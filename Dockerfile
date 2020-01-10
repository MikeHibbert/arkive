FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0
ENV DJANGO_ALLOWED_HOSTS "localhost 127.0.0.1 0.0.0.0 [::1]"
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN python -c "import nltk; nltk.download('punkt')"
RUN python /code/manage.py collectstatic --noinput
