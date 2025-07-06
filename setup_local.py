#!/usr/bin/env python3
"""
Setup script for Qiskit Hackathon local environment.
This script sets up the necessary environment to run Qiskit notebooks locally.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible!")
    return True

def main():
    print("🚀 Setting up Qiskit Hackathon local environment...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Try to create virtual environment if it doesn't exist
    venv_success = False
    if not os.path.exists("venv"):
        print("🏗️  Attempting to create virtual environment...")
        if run_command("python3 -m venv venv", "Creating virtual environment"):
            venv_success = True
        else:
            print("⚠️  Virtual environment creation failed. This might be due to missing python3-venv package.")
            print("   Proceeding with user-level installation...")
    else:
        venv_success = True
        print("✅ Virtual environment already exists")
    
    # Install requirements
    install_success = False
    if venv_success and os.path.exists("./venv/bin/pip"):
        if run_command("./venv/bin/pip install -r requirements.txt", "Installing Python dependencies in virtual environment"):
            install_success = True
    
    if not install_success:
        print("\n💡 Trying user-level installation...")
        if run_command("pip3 install --user -r requirements.txt --break-system-packages", "Installing with pip3 --user --break-system-packages"):
            install_success = True
        elif run_command("python3 -m pip install --user -r requirements.txt --break-system-packages", "Installing with python3 -m pip --user --break-system-packages"):
            install_success = True
    
    if not install_success:
        print("❌ Failed to install dependencies. Please try manual installation:")
        print("   pip3 install --user qiskit jupyter matplotlib numpy")
        sys.exit(1)
    
    # Enable Jupyter extensions
    venv_jupyter = "./venv/bin/jupyter"
    if os.path.exists(venv_jupyter):
        run_command(f"{venv_jupyter} nbextension enable --py widgetsnbextension", "Enabling Jupyter widgets")
    else:
        run_command("jupyter nbextension enable --py widgetsnbextension", "Enabling Jupyter widgets")
    
    # Create exercises directory in current path if needed
    if not os.path.exists("./exercises_levels"):
        os.makedirs("./exercises_levels/Gates_and_Circuits/Single Qubit Gates/Level_1_Single_Qubit_Gates", exist_ok=True)
        print("📁 Created exercises directory structure")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📚 To get started:")
    print("   1. Navigate to the Exercises directory: cd Exercises")
    print("   2. Start Jupyter notebook: jupyter notebook")
    print("   3. Open any of the .ipynb files to start learning!")
    print("\n💡 Note: For IBM Quantum access, you'll need to set up your IBM Quantum account")
    print("   Visit: https://quantum-computing.ibm.com/ to create an account and get your API token")

if __name__ == "__main__":
    main()