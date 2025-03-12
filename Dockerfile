FROM python:3.12-slim

WORKDIR /app

# Install wget for healthcheck
RUN apt-get update && apt-get install -y wget && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY writer ./writer/
COPY .streamlit ./.streamlit/
COPY app.py .
COPY .env .env
COPY docker_entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x docker_entrypoint.sh

# Expose the port the app runs on
EXPOSE 8085

# Set environment variable to indicate Docker environment
ENV DOCKER_CONTAINER=true
# Set Python to unbuffered mode to ensure logs are output immediately
ENV PYTHONUNBUFFERED=1
# Set Streamlit to log to stdout
ENV STREAMLIT_LOG_LEVEL=info

# Command to run the application
CMD ["./docker_entrypoint.sh"]
