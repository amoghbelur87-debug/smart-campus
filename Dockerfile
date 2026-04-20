# Use the official lightweight Python image.
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
# Ensure modules are searched for in the current directory
ENV PYTHONPATH /app

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup.
# We use gunicorn with 1 worker and 8 threads.
# We bind specifically to 0.0.0.0 to ensure it is externally accessible.
# The $PORT variable is provided by Cloud Run.
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
