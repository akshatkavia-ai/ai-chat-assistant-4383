#!/bin/bash
# CORS Verification Script
# Tests CORS configuration for the backend service

BACKEND_URL="https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001"
FRONTEND_ORIGIN="https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000"

echo "=========================================="
echo "CORS Configuration Test"
echo "=========================================="
echo "Backend URL: $BACKEND_URL"
echo "Frontend Origin: $FRONTEND_ORIGIN"
echo ""

echo "Test 1: OPTIONS Preflight Request to /conversations"
echo "---------------------------------------------------"
curl -i -X OPTIONS "$BACKEND_URL/conversations" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Access-Control-Request-Method: GET" \
  2>&1 | grep -E "HTTP/|access-control|Disallowed"
echo ""

echo "Test 2: GET Request to /conversations"
echo "--------------------------------------"
curl -i "$BACKEND_URL/conversations" \
  -H "Origin: $FRONTEND_ORIGIN" \
  2>&1 | grep -E "HTTP/|access-control"
echo ""

echo "Test 3: OPTIONS Preflight Request to /chat"
echo "-------------------------------------------"
curl -i -X OPTIONS "$BACKEND_URL/chat" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  2>&1 | grep -E "HTTP/|access-control|Disallowed"
echo ""

echo "Test 4: Health Check with CORS Info"
echo "------------------------------------"
curl -s "$BACKEND_URL/health" | python3 -m json.tool 2>&1 | grep -A 10 "cors"
echo ""

echo "=========================================="
echo "Test Complete"
echo "=========================================="
echo ""
echo "Expected Results:"
echo "- All OPTIONS requests should return 200 OK"
echo "- Should see 'access-control-allow-origin: $FRONTEND_ORIGIN'"
echo "- Should see 'access-control-allow-credentials: true'"
echo "- Should NOT see 'Disallowed CORS origin'"
