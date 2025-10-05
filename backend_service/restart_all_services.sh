#!/bin/bash
# Restart both frontend and backend services
# Ensures .env changes are picked up

set -e

echo "=========================================="
echo "Restarting Frontend and Backend Services"
echo "=========================================="
echo ""

# Stop backend
echo "1. Stopping backend service..."
pkill -f "uvicorn src.api.main:app" || true
sleep 2

# Stop frontend
echo "2. Stopping frontend service..."
pkill -f "react-scripts start" || true
sleep 2

# Start backend
echo "3. Starting backend service on port 3001..."
cd /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service
if [ -d "venv" ]; then
    source venv/bin/activate
    nohup uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload > backend.log 2>&1 &
    echo "   Backend started (PID: $!)"
else
    echo "   ERROR: venv not found!"
    exit 1
fi

sleep 3

# Start frontend
echo "4. Starting frontend service on port 4000..."
cd /home/kavia/workspace/code-generation/ai-chat-assistant-4382/frontend_client
nohup npm start > frontend.log 2>&1 &
echo "   Frontend started (PID: $!)"

sleep 5

echo ""
echo "=========================================="
echo "Services Restarted"
echo "=========================================="
echo ""
echo "Frontend: https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000"
echo "Backend:  https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001"
echo "API Docs: https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001/docs"
echo ""
echo "Check logs:"
echo "  Backend:  tail -f /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service/backend.log"
echo "  Frontend: tail -f /home/kavia/workspace/code-generation/ai-chat-assistant-4382/frontend_client/frontend.log"
echo ""
echo "Verify CORS:"
echo "  cd /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service"
echo "  ./verify_cors.sh"
