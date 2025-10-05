#!/bin/bash
# Restart script for backend service
# This script stops the running backend and restarts it with reload enabled

echo "Stopping existing backend service..."
pkill -f "uvicorn src.api.main:app"
sleep 2

echo "Starting backend service with auto-reload..."
cd /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service
source venv/bin/activate
nohup uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload > backend.log 2>&1 &

echo "Backend service restarted. Check backend.log for status."
echo "Service should be available at: https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001"
