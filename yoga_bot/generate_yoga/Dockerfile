FROM python:3.12.3
WORKDIR /generate_yoga
COPY . .
ENV FLASK_APP=generate_yoga.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["flask", "run"]