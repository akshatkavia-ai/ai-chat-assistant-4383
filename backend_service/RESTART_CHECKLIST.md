# Service Restart Checklist

Use this checklist to ensure proper restart after CORS configuration changes.

## Pre-Restart Verification

- [ ] Verify backend .env file is updated
  ```bash
  cat /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service/.env
  ```
  Should contain: `ALLOWED_ORIGINS=...https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000...`

- [ ] Verify frontend .env file is updated
  ```bash
  cat /home/kavia/workspace/code-generation/ai-chat-assistant-4382/frontend_client/.env
  ```
  Should contain: `REACT_APP_BACKEND_URL=https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001`

## Backend Restart

- [ ] Stop existing backend service
  ```bash
  pkill -f "uvicorn src.api.main:app"
  ```

- [ ] Start backend service
  ```bash
  cd /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service
  source venv/bin/activate
  nohup uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload > backend.log 2>&1 &
  ```

- [ ] Verify backend is running
  ```bash
  ps aux | grep uvicorn | grep -v grep
  ```

- [ ] Check backend startup logs
  ```bash
  tail -50 backend.log
  ```
  Look for: "CORS middleware configured with 6 allowed origins"

- [ ] Test backend health endpoint
  ```bash
  curl -s https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3001/health | grep -A 5 cors
  ```

## Frontend Restart

- [ ] Stop existing frontend service
  ```bash
  pkill -f "react-scripts start"
  # OR use your specific process manager command
  ```

- [ ] Start frontend service
  ```bash
  cd /home/kavia/workspace/code-generation/ai-chat-assistant-4382/frontend_client
  # Use your specific start command, e.g.:
  npm start &
  # OR your process manager command
  ```

- [ ] Verify frontend is running
  ```bash
  ps aux | grep "react-scripts" | grep -v grep
  ```

- [ ] Open frontend in browser
  ```
  https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000
  ```

## Post-Restart Verification

- [ ] Run CORS test script
  ```bash
  cd /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service
  ./test_cors.sh
  ```
  All tests should pass with 200 status codes

- [ ] Test from browser
  - [ ] Open frontend URL in browser
  - [ ] Open browser DevTools (F12) → Console tab
  - [ ] Try to send a chat message
  - [ ] Verify no CORS errors appear in console
  - [ ] Verify chat message is sent and response received

- [ ] Check network requests in browser
  - [ ] Open DevTools → Network tab
  - [ ] Send a chat message
  - [ ] Click on the /chat request
  - [ ] Verify Response Headers include:
    - `access-control-allow-origin: https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000`
    - `access-control-allow-credentials: true`

- [ ] Test all endpoints
  - [ ] GET /conversations - Should return conversation list
  - [ ] POST /chat - Should send message and get response
  - [ ] GET /history - Should retrieve conversation history (if conversations exist)

## Troubleshooting (if verification fails)

If any checks fail:

1. [ ] Review backend.log for errors
   ```bash
   tail -100 /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service/backend.log
   ```

2. [ ] Verify .env files weren't modified during restart
   ```bash
   cat /home/kavia/workspace/code-generation/ai-chat-assistant-4383/backend_service/.env
   cat /home/kavia/workspace/code-generation/ai-chat-assistant-4382/frontend_client/.env
   ```

3. [ ] Check for port conflicts
   ```bash
   netstat -tulpn | grep -E "3001|4000"
   ```

4. [ ] Clear browser cache and try again
   - Hard reload: Ctrl+Shift+R
   - Or use incognito/private mode

5. [ ] Refer to detailed documentation:
   - `COMPLETE_FIX_GUIDE.md` - Full troubleshooting guide
   - `CORS_FIX_SUMMARY.md` - CORS-specific documentation

## Sign-off

- [ ] All backend checks passed
- [ ] All frontend checks passed
- [ ] All post-restart verification checks passed
- [ ] Tested end-to-end chat functionality successfully
- [ ] No CORS errors in browser console
- [ ] Services are stable and responsive

**Completed by**: ________________
**Date**: ________________
**Time**: ________________
**Notes**: ________________________________________________
```

Task completed successfully! ✅
