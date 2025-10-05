# CORS Fix - Quick Reference Card

## URLs
- **Frontend**: https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000
- **Backend**: https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001
- **Backend API Docs**: https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001/docs
- **Backend Health**: https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001/health

## Quick Restart Commands

### Restart Backend
```bash
cd /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service
./restart.sh
```

### Restart Frontend
```bash
cd /home/kavia/workspace/code-generation/ai-chat-assistant-4382/frontend_client
# Kill existing: pkill -f "react-scripts start"
# Restart: npm start &
```

## Quick Test Commands

### Test CORS
```bash
cd /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service
./test_cors.sh
```

### Test Health
```bash
curl -s https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001/health | python3 -m json.tool
```

### Test Conversations
```bash
curl -i https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001/conversations \
  -H "Origin: https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000"
```

## Environment Variables

### Backend (.env)
```env
GEMINI_API_KEY=AIzaSyD798R-xKZTDjgsmNjvFr-IDRxfcwS1rEk
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4000,https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3000,https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000,...
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001
```

## Success Indicators

✅ Backend logs show: "CORS middleware configured with 6 allowed origins"
✅ Health endpoint returns CORS config with correct origins
✅ cURL tests return 200 with access-control-allow-origin header
✅ Frontend loads without CORS errors in browser console
✅ Chat messages send and receive successfully

## Failure Indicators

❌ "Disallowed CORS origin" in response
❌ No access-control-allow-origin header in response
❌ CORS errors in browser console
❌ 4XX or 5XX status codes on OPTIONS requests
❌ Backend logs don't show the expected CORS origins

## Documentation Files
- `COMPLETE_FIX_GUIDE.md` - Full step-by-step guide
- `CORS_FIX_SUMMARY.md` - Detailed CORS documentation
- `QUICK_REFERENCE.md` - This file
- `../README.md` - Project README with troubleshooting
