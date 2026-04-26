#!/bin/bash
# start.sh for Railway deployment

# Fail on error
set -e

# Default port to 8000 if not set by environment
PORT=${PORT:-7860}

echo "Starting FastAPI Todo App on port $PORT..."

# Use gunicorn with uvicorn workers for production
# -w 4: 4 worker processes
# -k uvicorn.workers.UvicornWorker: Use uvicorn workers
# --bind 0.0.0.0:$PORT: Bind to all interfaces on the dynamic port
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app --bind 0.0.0.0:$PORT --timeout 120
