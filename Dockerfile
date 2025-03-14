FROM python:3.12-slim

WORKDIR /app

# Install wget for healthcheck and dos2unix for line ending conversion
RUN apt-get update && apt-get install -y wget dos2unix && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY writer ./writer/
COPY .streamlit ./.streamlit/
COPY app.py .
COPY .env .env
COPY docker_entrypoint.sh .

# Fix line endings and make the entrypoint script executable
RUN dos2unix docker_entrypoint.sh && chmod +x docker_entrypoint.sh

# Expose the port the app runs on
EXPOSE 8085

# Set environment variable to indicate Docker environment
ENV DOCKER_CONTAINER=true
# Set Python to unbuffered mode to ensure logs are output immediately
ENV PYTHONUNBUFFERED=1
# Set Streamlit logger level using the new format
ENV STREAMLIT_LOGGER_LEVEL=info

# Command to run the application
CMD ["./docker_entrypoint.sh"]
