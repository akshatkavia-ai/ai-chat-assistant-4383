#!/bin/bash
# CORS Verification Script - Enhanced
# Tests CORS configuration for the backend service with actual frontend origin

BACKEND_HOST="vscode-internal-25292-beta.beta01.cloud.kavia.ai"
BACKEND_PORT="3001"
BACKEND_URL="https://${BACKEND_HOST}:${BACKEND_PORT}"

FRONTEND_HOST="vscode-internal-25292-beta.beta01.cloud.kavia.ai"
FRONTEND_PORT="4000"
FRONTEND_ORIGIN="https://${FRONTEND_HOST}:${FRONTEND_PORT}"

echo "=========================================="
echo "CORS Configuration Verification"
echo "=========================================="
echo "Backend URL: $BACKEND_URL"
echo "Frontend Origin: $FRONTEND_ORIGIN"
echo ""

echo "Test 1: OPTIONS Preflight for /conversations"
echo "----------------------------------------------"
curl -i -X OPTIONS "$BACKEND_URL/conversations" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: content-type" \
  2>&1 | grep -E "HTTP/|access-control-allow-origin|access-control-allow-credentials|access-control-allow-methods"
echo ""

echo "Test 2: OPTIONS Preflight for /chat"
echo "------------------------------------"
curl -i -X OPTIONS "$BACKEND_URL/chat" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  2>&1 | grep -E "HTTP/|access-control-allow-origin|access-control-allow-credentials|access-control-allow-methods"
echo ""

echo "Test 3: GET /conversations with Origin header"
echo "----------------------------------------------"
curl -i -X GET "$BACKEND_URL/conversations" \
  -H "Origin: $FRONTEND_ORIGIN" \
  2>&1 | grep -E "HTTP/|access-control-allow-origin|access-control-allow-credentials"
echo ""

echo "Test 4: POST /chat with Origin header"
echo "--------------------------------------"
curl -i -X POST "$BACKEND_URL/chat" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test CORS"}' \
  2>&1 | grep -E "HTTP/|access-control-allow-origin|access-control-allow-credentials"
echo ""

echo "Test 5: Backend Health Check"
echo "-----------------------------"
curl -s "$BACKEND_URL/health" | python3 -c "import sys, json; data=json.load(sys.stdin); print('CORS Origins:', json.dumps(data.get('cors', {}).get('allowed_origins', []), indent=2))"
echo ""

echo "=========================================="
echo "Verification Complete"
echo "=========================================="
echo ""
echo "✓ All tests should return HTTP 200"
echo "✓ Should see: access-control-allow-origin: $FRONTEND_ORIGIN"
echo "✓ Should see: access-control-allow-credentials: true"
echo "✓ Should see: access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"
