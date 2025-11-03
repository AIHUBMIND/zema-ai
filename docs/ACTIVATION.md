# Activating Virtual Environment

## Windows (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Windows (Command Prompt)
```cmd
venv\Scripts\activate.bat
```

## Windows (Git Bash)
```bash
source venv/Scripts/activate
```

## After Activation
Once activated, you'll see `(venv)` in your prompt, and you can use:
- `pip list` - List installed packages
- `pip install <package>` - Install packages
- `pip install -r requirements.txt` - Install all requirements

## Without Activation (Windows)
You can also use the full path:
```powershell
.\venv\Scripts\python.exe -m pip list
```

