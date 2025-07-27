#!/usr/bin/env python3
"""
Install dependencies in Anki's Python environment
Run this script to install required packages for the Japanese Pitch Accent addon.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install dependencies in Anki's Python environment"""
    
    # Path to Anki's Python environment
    anki_python = "/Users/ericstine/Library/Application Support/AnkiProgramFiles/.venv/bin/pip"
    
    # Check if Anki's Python exists
    if not os.path.exists(anki_python):
        print("❌ Error: Could not find Anki's Python environment")
        print(f"Expected path: {anki_python}")
        return False
    
    print("📦 Installing dependencies in Anki's Python environment...")
    print(f"Using: {anki_python}")
    
    try:
        # Install requirements
        result = subprocess.run([
            anki_python, "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            print("📋 Installed packages:")
            for line in result.stdout.split('\n'):
                if 'Successfully installed' in line:
                    print(f"   {line}")
            return True
        else:
            print("❌ Error installing dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_imports():
    """Test that all imports work"""
    print("\n🧪 Testing imports...")
    
    try:
        # Test SudachiPy import
        import sudachipy
        print("✅ SudachiPy imported successfully")
        
        # Test our modules
        from pitch_db import PitchDB
        from pitch_tokenizer import JapaneseTokenizer
        print("✅ All addon modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Japanese Pitch Accent Addon - Dependency Installer")
    print("=" * 50)
    
    if install_dependencies():
        if test_imports():
            print("\n🎉 All dependencies installed and working!")
            print("You can now restart Anki and the addon should work.")
        else:
            print("\n⚠️ Dependencies installed but imports failed.")
            print("Please check the error messages above.")
    else:
        print("\n❌ Failed to install dependencies.")
        sys.exit(1) 