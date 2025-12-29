# 部署到 GitHub 的 PowerShell 脚本
# 使用方法: .\deploy.ps1 "commit message"

param(
    [string]$Message = "Update application"
)

Write-Host "==================================" -ForegroundColor Green
Write-Host "   冲刷深度计算器 - GitHub 部署   " -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""

# 检查是否在正确的目录
if (-not (Test-Path "app.py")) {
    Write-Host "错误: 未找到 app.py 文件，请在项目根目录运行此脚本" -ForegroundColor Red
    exit 1
}

Write-Host "1. 检查 Git 状态..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "2. 添加所有文件..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "3. 提交更改: $Message" -ForegroundColor Yellow
git commit -m "$Message"

Write-Host ""
Write-Host "4. 推送到 GitHub..." -ForegroundColor Yellow
git push

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "   部署完成！                    " -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor Cyan
Write-Host "1. 访问 https://share.streamlit.io/" -ForegroundColor White
Write-Host "2. 登录后选择 'New app'" -ForegroundColor White
Write-Host "3. 选择仓库: wmwyy/cssdjs" -ForegroundColor White
Write-Host "4. 主文件: app.py" -ForegroundColor White
Write-Host "5. 点击 'Deploy'" -ForegroundColor White
Write-Host ""
Write-Host "本地测试:" -ForegroundColor Cyan
Write-Host "streamlit run app.py" -ForegroundColor White
Write-Host ""
