FROM python:3.12.3
WORKDIR /call_model
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x call_model.py
CMD ["python", "-u", "call_model.py"]