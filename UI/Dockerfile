FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY gradio_1.py .
CMD ["python","gradio_1.py"]