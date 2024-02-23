# Use the official Python image as base
FROM python:3.9.0

# Set the working directory in the container
WORKDIR /app


COPY diabetes /app/diabetes

WORKDIR /app/diabetes


# Install poetry
RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

RUN pip install python-multipart



# Copy your application files to the container
COPY deployment  /app/deployment

WORKDIR /app/deployment/instrument


RUN poetry install --no-root


# Run your FastAPI application using uvicorn
CMD ["python", "metrics/metrics.py"]