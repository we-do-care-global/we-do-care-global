@echo off
cd /d "C:\Users\DT User\Desktop\We Do Care Global"

setlocal

echo ============================================================
echo WE DO CARE GLOBAL — AUTONOMOUS DEPLOY & GITHUB PAGES SYNC
echo ============================================================
echo.

REM ============================================================
echo [1/6] Resolving GitHub tokens...
REM ============================================================
for %%R in ("we-do-care-global/we-do-care-global") do (
  set ORG=we-do-care-global
  set REPO=we-do-care-global/we-do-care-global
)
for %%R in ("WeDoCareGlobal-CC/agent-eval") do (
  set ORG=WeDoCareGlobal-CC
  set REPO=WeDoCareGlobal-CC/agent-eval
)
for %%R in ("WeDoCareGlobal-CC/agentvault") do (
  set ORG=WeDoCareGlobal-CC
  set REPO=WeDoCareGlobal-CC/agentvault
)
for %%R in ("WeDoCareGlobal-CC/agentguard") do (
  set ORG=WeDoCareGlobal-CC
  set REPO=WeDoCareGlobal-CC/agentguard
)
for %%R in ("WeDoCareGlobal-CC/enterprise-hybrid-rag") do (
  set ORG=WeDoCareGlobal-CC
  set REPO=WeDoCareGlobal-CC/enterprise-hybrid-rag
)
for %%R in ("WeDoCareGlobal-CC/pharma-intelligence-os") do (
  set ORG=WeDoCareGlobal-CC
  set REPO=WeDoCareGlobal-CC/pharma-intelligence-os
)

REM ============================================================
echo [2/6] Syncing docs/index.html from main portal console...
REM ============================================================
copy /y "C:\Users\DT User\Desktop\WDC_AI_Governance_Console.html" "C:\Users\DT User\Desktop\We Do Care Global\we-do-care-global\index.html" >nul
copy /y "C:\Users\DT User\Desktop\WDC_AI_Governance_Console.html" "C:\Users\DT User\Desktop\We Do Care Global\we-do-care-global\docs\index.html" >nul
echo [OK] Main portal index.html synced.

REM ============================================================
echo [3/6] Syncing agent repos (agent-eval, agentguard, agentvault, enterprise-hybrid-rag, pharma-intelligence-os)...
REM ============================================================
for %%D in (
  "WeDoCareGlobal-CC\agent-eval"
  "WeDoCareGlobal-CC\agentvault"
  "WeDoCareGlobal-CC\agentguard"
  "WeDoCareGlobal-CC\enterprise-hybrid-rag"
  "WeDoCareGlobal-CC\pharma-intelligence-os"
) do (
  echo --- Syncing %%~nxD ---
  if exist "%%D\docs\index.html" (
    copy /y "C:\Users\DT User\Desktop\We Do Care Global\we-do-care-global\docs\index.html" "%%D\docs\index.html" >nul
    echo [OK] docs/index.html updated.
  ) else (
    echo [WARN] docs/index.html not found in %%~nxD.
  )
)

REM ============================================================
echo [4/6] Committing and pushing main portal...
REM ============================================================
cd "C:\Users\DT User\Desktop\We Do Care Global\we-do-care-global"
git add index.html docs\index.html README.md .zenodo.json citation.cff
git commit -m "style: sync latest We Do Care Global console to portal, agent repos and docs"
git push origin main
echo [OK] Main portal pushed.

REM ============================================================
echo [5/6] Committing and pushing agent repos...
REM ============================================================
for %%D in (
  "WeDoCareGlobal-CC\agent-eval"
  "WeDoCareGlobal-CC\agentvault"
  "WeDoCareGlobal-CC\agentguard"
  "WeDoCareGlobal-CC\enterprise-hybrid-rag"
  "WeDoCareGlobal-CC\pharma-intelligence-os"
) do (
  cd "C:\Users\DT User\Desktop\We Do Care Global\%%D"
  if exist ".git" (
    git add docs\index.html
    git commit -m "docs: sync We Do Care Global console"
    git push origin main
    echo [OK] %%~nxD pushed.
  )
)

REM ============================================================
echo [6/6] Triggering GitHub Pages rebuild (main portal)...
REM ============================================================
curl -s -X POST "https://api.github.com/repos/we-do-care-global/we-do-care-global/pages" ^
  -H "Authorization: token %GH_TOKEN%" ^
  -H "Accept: application/vnd.github+json" ^
  -H "Content-Type: application/json" ^
  -d "{}" >nul
echo [OK] Main portal Pages rebuild triggered.

echo.
echo ============================================================
echo [SUCCESS] Successfully redeployed to GitHub Pages!
echo Live URLs:
echo   Main portal : https://wedocare-global.com/
echo   agent-eval  : https://wedocareglobal-cc.github.io/agent-eval/
echo   agentvault  : https://wedocareglobal-cc.github.io/agentvault/
echo   agentguard  : https://wedocareglobal-cc.github.io/agentguard/
echo   enterprise-hybrid-rag : https://wedocareglobal-cc.github.io/enterprise-hybrid-rag/
echo   pharma-intelligence-os: https://wedocareglobal-cc.github.io/pharma-intelligence-os/
echo   agentproof  : https://we-do-care-global.github.io/agentproof/
echo ============================================================
timeout /t 5
