FROM python:3
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential \
 && pip install python-telegram-bot \
 && pip install requests \
 && pip install emoji
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["core.py"]