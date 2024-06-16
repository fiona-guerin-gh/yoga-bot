FROM python:3.12.3
WORKDIR /yoga-bot
COPY . /yoga-bot
ENV FLASK_APP=yoga_bot.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["flask", "run"]