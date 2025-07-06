#!/usr/bin/env python3
"""
Setup script for Replicate integration with Qiskit Hackathon
Installs dependencies and helps configure API keys.
"""

import subprocess
import sys
import os
import shutil

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Replicate Integration for Qiskit Hackathon")
    print("=" * 60)
    
    # Check if pip is available
    if not shutil.which('pip'):
        print("❌ pip not found. Please install Python and pip first.")
        sys.exit(1)
    
    # Install requirements
    print("\n📦 Installing Python packages...")
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("⚠️  Some packages may have failed to install. You may need to:")
        print("   - Use pip3 instead of pip")
        print("   - Install in a virtual environment")
        print("   - Install missing system dependencies")
    
    # Set up environment file
    print("\n🔧 Setting up environment configuration...")
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("📝 Please edit .env and add your Replicate API token")
        else:
            # Create basic .env file
            with open('.env', 'w') as f:
                f.write("# Replicate API Configuration\n")
                f.write("REPLICATE_API_TOKEN=your_replicate_api_token_here\n")
                f.write("\n# Optional: OpenAI API for additional AI features\n")
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            print("✅ Created basic .env file")
    else:
        print("✅ .env file already exists")
    
    # Test installation
    print("\n🧪 Testing installation...")
    try:
        import qiskit
        import replicate
        import numpy as np
        print("✅ Core packages imported successfully")
        print(f"   - Qiskit version: {qiskit.__version__}")
        print(f"   - NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"⚠️  Import test failed: {e}")
        print("   Some packages may not be properly installed")
    
    # Create replicate_apps directory if it doesn't exist
    if not os.path.exists('replicate_apps'):
        os.makedirs('replicate_apps')
        print("✅ Created replicate_apps directory")
    
    # Make demo script executable
    if os.path.exists('replicate_apps/demo.py'):
        if os.name != 'nt':  # Not Windows
            os.chmod('replicate_apps/demo.py', 0o755)
        print("✅ Made demo script executable")
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Get a Replicate API token:")
    print("   - Visit https://replicate.com")
    print("   - Sign up for an account")
    print("   - Generate an API token")
    print("\n2. Configure your environment:")
    print("   - Edit the .env file")
    print("   - Replace 'your_replicate_api_token_here' with your actual token")
    print("\n3. Test the integration:")
    print("   - Run: python replicate_apps/demo.py")
    print("   - Or open the Jupyter notebook: Exercises/AI_Enhanced_Quantum_Computing.ipynb")
    print("\n4. Start building your hackathon project!")
    print("   - Use the quantum_ai_helper module in your code")
    print("   - Check out the examples and hackathon ideas")
    
    print("\n💡 Hackathon Project Ideas:")
    print("   - Quantum education assistant with AI explanations")
    print("   - Circuit optimizer using machine learning")
    print("   - Quantum art generator using AI image models")
    print("   - Natural language quantum programming interface")
    print("   - Quantum debugging assistant")

if __name__ == "__main__":
    main()