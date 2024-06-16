FROM python:3.12.3
WORKDIR /yoga-bot
COPY . /yoga-bot
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "pipeline.py"]
