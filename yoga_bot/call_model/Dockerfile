FROM python:3.12.3
WORKDIR /call_model
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3", "call_model.py"]