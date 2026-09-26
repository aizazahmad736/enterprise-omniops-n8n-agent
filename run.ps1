Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   Starting OmniOps Enterprise AI Agent Environment" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan

Write-Host "[1/3] Checking & Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install fastapi uvicorn pydantic requests --quiet

Write-Host "[2/3] Launching Enterprise Mock API Backend on http://localhost:8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn backend.mock_api:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 3

Write-Host "[3/3] Opening Interactive Dashboard..." -ForegroundColor Yellow
Start-Process "frontend\index.html"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " OmniOps System is LIVE!" -ForegroundColor Green
Write-Host " - Mock Enterprise Backend: http://localhost:8000"
Write-Host " - API Docs (Swagger):      http://localhost:8000/docs"
Write-Host " - Frontend Dashboard:      Opened in browser"
Write-Host " - n8n Workflow JSON:       workflows/omniops_agent_workflow.json"
Write-Host "======================================================================" -ForegroundColor Cyan
