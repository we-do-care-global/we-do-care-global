@echo off
cd /d "C:\Users\DT User\we-do-care-global"

echo ==============================================================
echo  WE DO CARE GLOBAL — AUTONOMOUS DEPLOY & GITHUB PAGES SYNC
echo ==============================================================
echo.

echo [1/4] Syncing Desktop console to repository index & docs...
copy /y "C:\Users\DT User\Desktop\WDC_AI_Governance_Console.html" "C:\Users\DT User\we-do-care-global\index.html" >nul
copy /y "C:\Users\DT User\Desktop\WDC_AI_Governance_Console.html" "C:\Users\DT User\we-do-care-global\docs\index.html" >nul
echo [OK] Files synced.

echo.
echo [2/4] Staging files for Git...
git add index.html docs/index.html README.md .zenodo.json citation.cff
git status -s

echo.
echo [3/4] Committing changes...
git commit -m "style: luxury obsidian velvet micro-noise background, authentic medallion branding, direct 6 sister platforms and admin auth"

echo.
echo [4/4] Pushing to GitHub main branch...
git push origin main

echo.
echo ==============================================================
echo [SUCCESS] Successfully redeployed to GitHub Pages!
echo Live URL: https://we-do-care-global.github.io/we-do-care-global/
echo ==============================================================
timeout /t 5
