FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0
ENV DJANGO_ALLOWED_HOSTS ".arkive.online"
RUN mkdir /code
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY . /code/
RUN python -c "import nltk; nltk.download('punkt')"
WORKDIR /code
RUN python manage.py collectstatic --noinput
