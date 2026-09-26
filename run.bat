@echo off
echo ======================================================================
echo    Starting OmniOps Enterprise AI Agent Environment
echo ======================================================================

echo [1/3] Installing Python dependencies...
python -m pip install fastapi uvicorn pydantic requests --quiet

echo [2/3] Launching Enterprise Mock API Backend on http://localhost:8000...
start "OmniOps Mock API" cmd /k "python -m uvicorn backend.mock_api:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

echo [3/3] Opening Interactive Dashboard...
start "" "frontend\index.html"

echo ======================================================================
echo  OmniOps System is LIVE!
echo  - Mock Enterprise Backend: http://localhost:8000
echo  - API Docs (Swagger):      http://localhost:8000/docs
echo  - Frontend Dashboard:      Opened in your default browser
echo  - n8n Workflow JSON:       workflows/omniops_agent_workflow.json
echo ======================================================================
pause
