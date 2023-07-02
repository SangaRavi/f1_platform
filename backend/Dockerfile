# Set base image (Python 3.9)
FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y default-jre

# Copy list of backend requirements
COPY requirements-backend.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

ENV CURRENT_ENV="db"

COPY . /app

# Expose port
EXPOSE 5000:5000

CMD uvicorn main:app --host 0.0.0.0 --port 5000 --reload