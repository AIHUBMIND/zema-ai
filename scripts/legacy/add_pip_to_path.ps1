# PowerShell script to add pip to PATH permanently
# Run this script as Administrator or it will add to User PATH

$scriptsPath = "C:\Users\abrah\AppData\Local\Python\pythoncore-3.14-64\Scripts"

# Check if pip.exe exists
if (Test-Path "$scriptsPath\pip.exe") {
    Write-Host "Found pip.exe at: $scriptsPath" -ForegroundColor Green
    
    # Get current PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    # Check if already in PATH
    if ($currentPath -like "*$scriptsPath*") {
        Write-Host "Scripts folder is already in PATH!" -ForegroundColor Yellow
        Write-Host "Current PATH includes: $scriptsPath" -ForegroundColor Yellow
    } else {
        # Add to User PATH
        Write-Host "Adding to User PATH..." -ForegroundColor Cyan
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$scriptsPath", "User")
        
        # Also add to current session
        $env:Path += ";$scriptsPath"
        
        Write-Host "Added $scriptsPath to PATH" -ForegroundColor Green
        Write-Host ""
        Write-Host "Note: You may need to restart your terminal for changes to take effect." -ForegroundColor Yellow
        Write-Host "Or run: refreshenv" -ForegroundColor Yellow
    }
    
    # Test pip
    Write-Host ""
    Write-Host "Testing pip..." -ForegroundColor Cyan
    & "$scriptsPath\pip.exe" --version
    
} else {
    Write-Host "pip.exe not found at: $scriptsPath" -ForegroundColor Red
    Write-Host "Please check your Python installation path." -ForegroundColor Red
}
