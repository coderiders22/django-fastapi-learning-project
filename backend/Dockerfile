FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Requirements are already at root (because workdir=backend)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy everything (config/, calculator/, manage.py, start.sh)
COPY . .

# Make sure start.sh is executable
RUN chmod +x start.sh

# Koyeb uses 8080
EXPOSE 8080

CMD ["bash", "start.sh"]
