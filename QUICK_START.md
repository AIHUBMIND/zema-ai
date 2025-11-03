# Quick Reference: Activating Virtual Environment

## For PowerShell (Current Shell)

Run this command in PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
.\venv\Scripts\Activate.ps1
```

## After Activation

You'll see `(venv)` in your prompt, and then you can use:
```powershell
pip list
pip install <package>
python scripts/test_setup.py
```

## Quick Test (Without Activation)

To test if everything works without activating:
```powershell
.\venv\Scripts\python.exe -m pip list
.\venv\Scripts\python.exe scripts/test_setup.py
```

