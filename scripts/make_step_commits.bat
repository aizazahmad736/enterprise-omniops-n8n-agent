@echo off
echo ======================================================================
echo  Rebuilding Step-by-Step Git Commit History for GitHub
echo ======================================================================

git config user.name "aizazahmad736"
git config user.email "aizazexforwardian@gmail.com"

git reset --mixed

echo [1/8] Committing project structure & environment templates...
git add .gitignore .env.example
git commit -m "chore: initialize enterprise-omniops project structure and git configuration"

echo [2/8] Committing backend requirements & core FastAPI app...
git add backend/requirements.txt
git commit -m "feat(backend): setup FastAPI dependencies and enterprise service scaffolding"

echo [3/8] Committing enterprise backend services & guardrailed refund engine...
git add backend/mock_api.py
git commit -m "feat(backend): implement CRM, policy RAG, order tracking, and guardrailed refund engine"

echo [4/8] Committing n8n LangChain AI Agent workflow definition...
git add workflows/omniops_agent_workflow.json
git commit -m "feat(agent): construct n8n LangChain AI Agent workflow with 6 enterprise tools and memory"

echo [5/8] Committing frontend playground & real-time telemetry dashboard...
git add frontend/index.html
git commit -m "feat(frontend): create interactive operations playground and real-time ReAct telemetry viewer"

echo [6/8] Committing verification test suite...
git add scripts/test_agent.py
git commit -m "test: implement automated end-to-end integration and policy guardrail verification suite"

echo [7/8] Committing Docker orchestration...
git add docker-compose.yml backend/Dockerfile
git commit -m "ci/docker: add multi-container Docker Compose and Dockerfile for n8n orchestration"

echo [8/8] Committing system documentation and startup scripts...
git add README.md run.bat run.ps1 scripts/
git commit -m "docs: add enterprise architecture specs, quickstart guide, and Windows startup scripts"

git branch -M main

echo ======================================================================
echo  8 Granular Commits Created Successfully!
echo ======================================================================
git log --oneline -n 8

echo.
echo Next step to push to GitHub:
echo 1. Create repository 'enterprise-omniops-n8n-agent' at https://github.com/new
echo 2. Run: git remote add origin https://github.com/aizazahmad736/enterprise-omniops-n8n-agent.git
echo 3. Run: git push -u origin main
pause
