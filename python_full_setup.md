# Python Full Setup Guide for macOS (Intel Mac)

This guide covers the complete Python setup process for Django microservice development on macOS.

## Prerequisites

- macOS with Intel processor
- Terminal access
- Internet connection

## Step 1: Install Homebrew

If not already installed, install Homebrew (package manager for macOS):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Verify installation:
```bash
brew --version
```

## Step 2: Install Python Versions via Homebrew

Install specific Python versions:

```bash
# Install Python 3.11
brew install python@3.11

# Install latest Python (3.13)
brew install python3
```

Verify installations:
```bash
/usr/local/bin/python3.11 --version  # Should show Python 3.11.13
/usr/local/bin/python3 --version     # Should show Python 3.13.x
```

## Step 3: Install pyenv for Version Management

Install pyenv for flexible Python version management:

```bash
brew install pyenv
```

Add pyenv to your shell configuration:
```bash
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

## Step 4: Configure PATH and Aliases

Add Homebrew Python to PATH and create useful aliases:

```bash
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
echo 'alias python311="/usr/local/bin/python3.11"' >> ~/.zshrc
echo 'alias python313="/usr/local/bin/python3.13"' >> ~/.zshrc
echo 'alias pip311="/usr/local/bin/pip3.11"' >> ~/.zshrc
echo 'alias pip313="/usr/local/bin/pip3.13"' >> ~/.zshrc
```

Reload shell configuration:
```bash
source ~/.zshrc
```

## Step 5: Install Python 3.11.5 via pyenv

Install and set Python 3.11.5 as global default:

```bash
pyenv install 3.11.5
pyenv global 3.11.5
```

## Step 6: Verify Complete Setup

Check all Python installations:

```bash
# pyenv managed Python (default)
python --version          # Should show Python 3.11.5
python3 --version         # Should show Python 3.11.5
which python              # Should show ~/.pyenv/shims/python

# Homebrew Python via aliases
python311 --version       # Should show Python 3.11.13
python313 --version       # Should show Python 3.13.7

# Direct Homebrew paths
/usr/local/bin/python3.11 --version
/usr/local/bin/python3 --version
```

## Step 7: Create Virtual Environment for Django Project

Navigate to your project directory and create a virtual environment:

```bash
cd /Users/guru/Desktop/micro_service_shop
python -m venv venv
source venv/bin/activate
```

Verify virtual environment:
```bash
python --version          # Should show Python 3.11.5
which python              # Should show venv path
```

## Step 8: Install Django and Dependencies

Inside your activated virtual environment:

```bash
# Install Django
pip install django

# Install Django REST framework for APIs
pip install djangorestframework

# Install CORS headers for microservices
pip install django-cors-headers

# Install database adapter (PostgreSQL example)
pip install psycopg2-binary

# Create requirements file
pip freeze > requirements.txt
```

## Step 9: VS Code Configuration

1. Open VS Code in your project directory:
   ```bash
   code .
   ```

2. Select Python interpreter:
   - Press `Cmd+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose the interpreter from your `venv` folder

## Daily Workflow

### Starting Development Session
```bash
cd /Users/guru/Desktop/micro_service_shop
source venv/bin/activate
# Your virtual environment is now active
```

### Installing New Packages
```bash
# Always ensure venv is activated first
pip install package_name
pip freeze > requirements.txt  # Update requirements
```

### Ending Development Session
```bash
deactivate  # Exit virtual environment
```

## Troubleshooting

### If Python version is wrong:
```bash
# Check what's being used
which python
python --version

# Reset pyenv if needed
pyenv rehash
pyenv global 3.11.5
```

### If virtual environment issues:
```bash
# Remove and recreate venv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Clean .zshrc if duplicates:
```bash
# Backup first
cp ~/.zshrc ~/.zshrc.backup

# Edit to remove duplicates
nano ~/.zshrc

# Reload
source ~/.zshrc
```

## Final Setup Summary

You now have:
- ✅ Homebrew package manager
- ✅ Multiple Python versions (3.11.13, 3.11.5, 3.13.7)
- ✅ pyenv for version management
- ✅ Proper PATH configuration
- ✅ Useful aliases for direct access
- ✅ Virtual environment for Django project
- ✅ Django and related packages installed
- ✅ VS Code integration ready

## Benefits of This Setup

1. **Flexibility**: Multiple Python versions available
2. **Isolation**: Virtual environments prevent conflicts
3. **Convenience**: Aliases for quick access
4. **Professional**: Industry-standard development setup
5. **Scalable**: Easy to manage multiple projects

Your Python environment is now optimized for Django microservice development! 🚀

# In your virtual environment
source venv/bin/activate

# Format single file
black test_formatting.py

# Format entire project
black .

# Organize imports
isort .

# Check linting
flake8 .

Cmd+Shift+P → "Format Document"
Cmd+Shift+P → "Organize Imports"
Cmd+Shift+P → "Python: Select Interpreter" (choose your venv)>
