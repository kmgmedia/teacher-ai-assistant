# AI Teaching Assistant - Quick Launch
Clear-Host
Write-Host "🎓 AI Teaching Assistant" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\DELL\Desktop\ai_assistant_for_teachers"

Write-Host "🚀 Launching dashboard..." -ForegroundColor Cyan
& ".venv\Scripts\streamlit.exe" run dashboard.py --server.port 8501

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Error occurred. Press any key to exit..." -ForegroundColor Red
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
