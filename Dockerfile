# Use an official Python 3.11 runtime as a parent image
FROM python:3.11.7-slim-bullseye
ENV PYTHONUNBUFFERED True


# Set the working directory in the container
WORKDIR /app
ENV HOST 0.0.0.0


# Install first part of packages
COPY requirements.txt /app
# RUN python -m pip install --upgrade pip
RUN pip install --default-timeout=100  -v -r requirements.txt


# Copy the current directory contents into the container at /app
COPY . /app
COPY pyproject.toml poetry.lock* /app/

# Disable virtualenvs created by Poetry
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
RUN poetry install --only main --no-interaction --no-ansi

# Make port 80 available to the world outside this container
EXPOSE 8080

# Set the entrypoint command to run Streamlit
CMD ["streamlit", "run", "app.py"]