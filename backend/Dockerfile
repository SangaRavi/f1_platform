# Set base image (Python 3.9)
FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y default-jre

# Copy list of backend requirements
COPY requirements-backend.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy files to working directory (into a newly created /app directory)
COPY . /app

# Expose port
EXPOSE 8000:8000

CMD uvicorn app:app --host 0.0.0.0 --port 8000 --reload