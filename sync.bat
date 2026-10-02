@echo off
cd /d "C:\Users\DT User\we-do-care-global"
echo [1/3] Adding files to git...
git add README.md docs/index.html index.html .zenodo.json citation.cff
git status
echo.
echo [2/3] Committing changes...
git commit -m "feat: deploy unified brand seal, Radix/shadcn design system, dynamic pipeline board and debugged auth"
echo.
echo [3/3] Pushing to GitHub main branch...
git push origin main
echo.
echo ==============================================================
echo [SUCCESS] Successfully redeployed to GitHub Pages!
echo URL: https://we-do-care-global.github.io/we-do-care-global/
echo ==============================================================
timeout /t 5
