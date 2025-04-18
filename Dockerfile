# Specify the base Python vertion
FROM python:3.12.3-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Set dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into a container
COPY . /app/

# Make database migrations (for SQLite) and build static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Open the port for the Django server
EXPOSE 8000

# To start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

