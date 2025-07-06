#!/bin/bash

# Qiskit Hackathon Local Start Script
echo "🚀 Starting Qiskit Hackathon notebooks locally..."

# Check if we're in the right directory
if [ ! -d "Exercises" ]; then
    echo "❌ Error: Exercises directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Check if virtual environment exists and has qiskit
if [ -d "venv" ] && ./venv/bin/python -c "import qiskit" 2>/dev/null; then
    echo "✅ Using virtual environment"
    PYTHON="./venv/bin/python"
    JUPYTER="./venv/bin/jupyter"
elif python3 -c "import qiskit" 2>/dev/null; then
    echo "✅ Using system Python"
    PYTHON="python3"
    # Check for jupyter in different locations
    if [ -f "$HOME/.local/bin/jupyter" ]; then
        JUPYTER="$HOME/.local/bin/jupyter"
    elif command -v jupyter >/dev/null 2>&1; then
        JUPYTER="jupyter"
    else
        JUPYTER="python3 -m jupyter"
    fi
else
    echo "⚠️  Qiskit not found. Installing dependencies..."
    python3 setup_local.py
    if [ -d "venv" ]; then
        PYTHON="./venv/bin/python"
        JUPYTER="./venv/bin/jupyter"
    else
        PYTHON="python3"
        if [ -f "$HOME/.local/bin/jupyter" ]; then
            JUPYTER="$HOME/.local/bin/jupyter"
        else
            JUPYTER="python3 -m jupyter"
        fi
    fi
fi

# Navigate to exercises and start Jupyter
echo "📁 Navigating to Exercises directory..."
cd Exercises

echo "🎯 Starting Jupyter Notebook..."
echo "📝 The notebook will open in your browser automatically."
echo "🔗 If it doesn't open, visit: http://localhost:8888"
echo ""
echo "💡 Tips:"
echo "   - Start with Easy_Single_Qubit_Gates.ipynb"
echo "   - Use Shift+Enter to run cells"
echo "   - For IBM Quantum access, get your token from: https://quantum-computing.ibm.com/"
echo ""

$JUPYTER notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root