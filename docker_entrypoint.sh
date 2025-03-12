#!/bin/bash
# Startup script for the AI Content Writer application in Docker

# Print a message to indicate we're starting
echo "==================================================="
echo "Starting AI Content Writer application in Docker container"
echo "==================================================="

# Set environment variables for better logging
export PYTHONUNBUFFERED=1
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_LOG_LEVEL=info

# Create a log file that we can tail
touch /app/docker.log

# Function to handle cleanup on exit
cleanup() {
    echo "Shutting down AI Content Writer..."
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGTERM SIGINT

# Add a custom log message that will definitely show up in Docker logs
echo "DOCKER LOG: About to start Streamlit application" >> /proc/1/fd/1
echo "DOCKER LOG: About to start Streamlit application" >> /proc/1/fd/2

# Run the Streamlit application in the background and redirect output to our log file
streamlit run app.py --server.port=8085 2>&1 &
APP_PID=$!

# Tail the log file to show logs in Docker
tail -f /app/docker.log &
TAIL_PID=$!

# Print a message to indicate the application is running
echo "==================================================="
echo "AI Content Writer application is now running"
echo "Access it at http://localhost:8085"
echo "==================================================="

# Wait for the application to exit
wait $APP_PID
kill $TAIL_PID
