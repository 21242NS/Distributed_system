FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY Lab1/mandelbrot_set.py Lab1/server.py ./

EXPOSE 8000
CMD ["python", "server.py"]