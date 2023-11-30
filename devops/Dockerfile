# Use an official Python runtime as a parent image
FROM python:3.10
LABEL maintainer="kaspar"

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
# RUN apt-get update && apt-get install postgresql-dev gcc python3-dev musl-dev

# Set the working directory to /app/
COPY . /app/
WORKDIR /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
