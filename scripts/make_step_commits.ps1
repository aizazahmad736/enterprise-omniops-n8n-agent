# Step-by-Step Git Commit Automation Script
# Breaks the OmniOps project into 8 incremental, professional commits for your GitHub contribution graph.

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " Rebuilding Step-by-Step Git Commit History for GitHub" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan

# Ensure git user is set
git config user.name "aizazahmad736"
git config user.email "aizazexforwardian@gmail.com"

# Reset existing commit if any, keeping all files in working directory
git reset --mixed

# Commit 1: Project Scaffolding
Write-Host "[1/8] Committing project structure & environment templates..." -ForegroundColor Yellow
git add .gitignore .env.example
git commit -m "chore: initialize enterprise-omniops project structure and git configuration"

# Commit 2: Backend API Core & Requirements
Write-Host "[2/8] Committing backend requirements & core FastAPI app..." -ForegroundColor Yellow
git add backend/requirements.txt
git commit -m "feat(backend): setup FastAPI dependencies and enterprise service scaffolding"

# Commit 3: Mock CRM, Orders, KB RAG & Policy Guardrails
Write-Host "[3/8] Committing enterprise backend services & guardrailed refund engine..." -ForegroundColor Yellow
git add backend/mock_api.py
git commit -m "feat(backend): implement CRM, policy RAG, order tracking, and guardrailed refund engine"

# Commit 4: n8n LangChain AI Agent Workflow
Write-Host "[4/8] Committing n8n LangChain AI Agent workflow definition..." -ForegroundColor Yellow
git add workflows/omniops_agent_workflow.json
git commit -m "feat(agent): construct n8n LangChain AI Agent workflow with 6 enterprise tools and memory"

# Commit 5: Interactive Web UI & ReAct Telemetry Stream
Write-Host "[5/8] Committing frontend playground & real-time telemetry dashboard..." -ForegroundColor Yellow
git add frontend/index.html
git commit -m "feat(frontend): create interactive operations playground and real-time ReAct telemetry viewer"

# Commit 6: Automated Test & Verification Suite
Write-Host "[6/8] Committing verification test suite..." -ForegroundColor Yellow
git add scripts/test_agent.py
git commit -m "test: implement automated end-to-end integration and policy guardrail verification suite"

# Commit 7: Docker Compose & Containerization
Write-Host "[7/8] Committing Docker orchestration..." -ForegroundColor Yellow
git add docker-compose.yml backend/Dockerfile
git commit -m "ci/docker: add multi-container Docker Compose and Dockerfile for n8n orchestration"

# Commit 8: Documentation & 1-Click Launchers
Write-Host "[8/8] Committing system documentation and startup scripts..." -ForegroundColor Yellow
git add README.md run.bat run.ps1 scripts/
git commit -m "docs: add enterprise architecture specs, quickstart guide, and Windows startup scripts"

# Rename branch to main
git branch -M main

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " 8 Granular Commits Created Successfully!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
git log --oneline -n 8

Write-Host ""
Write-Host "Next step to push to GitHub:" -ForegroundColor Yellow
Write-Host "1. Create repository 'enterprise-omniops-n8n-agent' at https://github.com/new"
Write-Host "2. Run: git remote add origin https://github.com/aizazahmad736/enterprise-omniops-n8n-agent.git"
Write-Host "3. Run: git push -u origin main"
