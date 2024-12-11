# Base Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port for Gunicorn
EXPOSE 8000

# Start the application
CMD ["gunicorn", "aysu_yildiz.wsgi:application", "--bind", "0.0.0.0:8000"]
