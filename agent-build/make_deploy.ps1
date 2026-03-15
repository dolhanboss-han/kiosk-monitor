# 빌드 후 배포 패키지 생성
 = "D:\BSEYE\agent-build\deploy"
if (Test-Path ) { Remove-Item  -Recurse -Force }
New-Item  -ItemType Directory | Out-Null
Copy-Item "D:\BSEYE\agent-build\dist\bseye-agent.exe" 
Copy-Item "D:\BSEYE\agent-build\config.ini" 
Copy-Item "D:\BSEYE\agent-build\templates" "\templates" -Recurse
Copy-Item "D:\BSEYE\agent-build\dist\thermal_checker.exe"
Write-Host "=== 배포 패키지 ==="
Get-ChildItem  -Recurse | Select-Object FullName | Format-Table -AutoSize
Write-Host "이 폴더(deploy)를 통째로 USB에 복사하세요"
