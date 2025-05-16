# Dockerfile
FROM python:alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the port
EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate
# Run server
CMD ["python manage.py runserver 0.0.0.0:8000"]
