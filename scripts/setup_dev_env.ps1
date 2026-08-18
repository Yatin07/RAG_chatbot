<#
.SYNOPSIS
    Sets up the development environment for RAG PDF Chatbot.
.DESCRIPTION
    This script automates the setup of the development environment including:
    - Creating a virtual environment
    - Installing dependencies
    - Setting up pre-commit hooks
    - Running initial tests
#>

param (
    [string]$PythonPath = "python"
)

function Write-Section {
    param([string]$Title)
    Write-Host "`n==========================================" -ForegroundColor Cyan
    Write-Host $Title -ForegroundColor Green
    Write-Host "==========================================`n" -ForegroundColor Cyan
}

function Write-Step {
    param([string]$Message)
    Write-Host "📋 $Message" -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

try {
    # Check if Python is available
    Write-Section "Checking Python Installation"
    Write-Step "Verifying Python installation..."
    $pythonVersion = & $PythonPath --version 2>&1
    if (-not $pythonVersion) {
        throw "Python not found. Please install Python 3.8+ and ensure it's in your PATH."
    }
    Write-Success "Python found: $pythonVersion"

    # Create virtual environment
    Write-Section "Setting Up Virtual Environment"
    Write-Step "Creating virtual environment..."
    if (Test-Path "venv") {
        Write-Host "Virtual environment already exists." -ForegroundColor Yellow
    } else {
        & $PythonPath -m venv venv
        Write-Success "Virtual environment created."
    }

    # Activate virtual environment
    Write-Step "Activating virtual environment..."
    if ($IsWindows) {
        & .\venv\Scripts\Activate.ps1
    } else {
        & source venv/bin/activate
    }
    Write-Success "Virtual environment activated."

    # Upgrade pip
    Write-Step "Upgrading pip..."
    & python -m pip install --upgrade pip
    Write-Success "Pip upgraded."

    # Install development dependencies
    Write-Section "Installing Dependencies"
    Write-Step "Installing development dependencies..."
    & pip install -e .[dev]
    Write-Success "Development dependencies installed."

    # Set up pre-commit hooks
    Write-Section "Setting Up Pre-Commit Hooks"
    Write-Step "Installing pre-commit..."
    & pre-commit install
    Write-Success "Pre-commit hooks installed."

    # Run pre-commit on all files
    Write-Step "Running pre-commit on all files..."
    & pre-commit run --all-files
    Write-Success "Pre-commit checks completed."

    # Run tests
    Write-Section "Running Tests"
    Write-Step "Running unit tests..."
    & pytest tests/ -v
    Write-Success "Tests completed."

    # Create .env file if it doesn't exist
    Write-Section "Setting Up Configuration"
    if (-not (Test-Path ".env")) {
        Write-Step "Creating .env file from template..."
        Copy-Item .env.example .env
        Write-Success ".env file created. Please review and modify as needed."
    } else {
        Write-Host ".env file already exists." -ForegroundColor Yellow
    }

    Write-Section "Setup Complete! 🎉"
    Write-Host "Your development environment is ready." -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Review and modify .env file as needed" -ForegroundColor Yellow
    Write-Host "2. Start coding! 🚀" -ForegroundColor Yellow
    Write-Host "3. Run tests with: pytest tests/" -ForegroundColor Yellow
    Write-Host "4. Run the application with: python -m src.main --help" -ForegroundColor Yellow

} catch {
    Write-Error "Setup failed: $_"
    Write-Error "Please check the error and try again."
    exit 1
}
