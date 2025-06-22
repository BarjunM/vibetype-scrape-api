#!/usr/bin/env python3
"""
Render Deployment Helper Script
"""
import os
import subprocess
import sys
import requests
import json

def check_git():
    """Check if git is installed and repository is initialized"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git is not installed. Please install Git first.")
            return False
        print("✅ Git is installed")
        return True
    except FileNotFoundError:
        print("❌ Git is not installed. Please install Git first.")
        return False

def check_git_repo():
    """Check if current directory is a git repository"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not a git repository. Initializing...")
            subprocess.run(['git', 'init'])
            subprocess.run(['git', 'add', '.'])
            subprocess.run(['git', 'commit', '-m', 'Initial commit for Render deployment'])
            print("✅ Git repository initialized")
        else:
            print("✅ Git repository found")
        return True
    except Exception as e:
        print(f"❌ Error checking git repository: {e}")
        return False

def check_github_remote():
    """Check if GitHub remote is configured"""
    try:
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if 'origin' not in result.stdout:
            print("⚠️  No GitHub remote found. You'll need to:")
            print("   1. Create a repository on GitHub")
            print("   2. Add it as remote: git remote add origin <your-github-url>")
            print("   3. Push your code: git push -u origin main")
            return False
        else:
            print("✅ GitHub remote configured")
            return True
    except Exception as e:
        print(f"❌ Error checking remote: {e}")
        return False

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ .env file not found. Creating template...")
        with open('.env', 'w') as f:
            f.write("# Environment variables for local development\n")
            f.write("# Copy this file and add your actual API keys\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("EMBEDDING_MODEL=text-embedding-3-small\n")
        print("✅ .env template created")
        print("⚠️  Please edit .env file and add your OpenAI API key")
    else:
        print("✅ .env file found")

def check_render_files():
    """Check if Render-specific files exist"""
    files_to_check = ['render.yaml', 'requirements.txt', 'main.py']
    missing_files = []
    
    for file in files_to_check:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_local_api():
    """Test if the API works locally"""
    print("🧪 Testing local API...")
    try:
        # Start the API in background
        process = subprocess.Popen(
            [sys.executable, 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for startup
        import time
        time.sleep(3)
        
        # Test health endpoint
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Local API test passed")
            process.terminate()
            return True
        else:
            print(f"❌ Local API test failed: {response.status_code}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Local API test failed: {e}")
        return False

def create_render_instructions():
    """Create step-by-step Render instructions"""
    instructions = """
RENDER DEPLOYMENT INSTRUCTIONS
===============================

Step 1: Prepare Your Repository
-------------------------------
1. Make sure your code is committed to git
2. Push to GitHub: git push origin main

Step 2: Sign Up for Render
--------------------------
1. Go to https://render.com
2. Sign up with your GitHub account
3. Verify your email address

Step 3: Create Web Service
--------------------------
1. Click "New +" -> "Web Service"
2. Connect your GitHub repository
3. Select your repository (vibetype-scrape-api)

Step 4: Configure the Service
-----------------------------
- Name: vibetype-scrape-api
- Environment: Python 3
- Build Command: pip install -r requirements.txt
- Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
- Plan: Free (or choose paid plan)

Step 5: Add Environment Variables
--------------------------------
Click "Environment" and add:
- Key: OPENAI_API_KEY
- Value: your_openai_api_key_here

Step 6: Deploy
--------------
1. Click "Create Web Service"
2. Wait for build to complete (2-5 minutes)
3. Your API will be available at: https://your-app-name.onrender.com

Step 7: Test Your Deployment
----------------------------
Run: python test_deployment.py https://your-app-name.onrender.com

Useful Links:
- Render Dashboard: https://dashboard.render.com
- OpenAI API Keys: https://platform.openai.com/api-keys
- Your API Documentation: https://your-app-name.onrender.com/docs
"""
    
    with open('RENDER_INSTRUCTIONS.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Render instructions saved to RENDER_INSTRUCTIONS.txt")

def main():
    """Main deployment helper function"""
    print("🚀 Render Deployment Helper")
    print("=" * 40)
    
    # Check prerequisites
    if not check_git():
        return
    
    if not check_git_repo():
        return
    
    if not check_github_remote():
        print("\n⚠️  Please set up GitHub remote before continuing")
        print("   git remote add origin <your-github-url>")
        print("   git push -u origin main")
        return
    
    if not check_render_files():
        return
    
    check_env_file()
    
    # Test local API (optional)
    test_choice = input("\n🧪 Test local API before deployment? (y/n): ").lower()
    if test_choice == 'y':
        test_local_api()
    
    # Create instructions
    create_render_instructions()
    
    print("\n🎯 Ready for Render deployment!")
    print("📖 Check RENDER_INSTRUCTIONS.txt for detailed steps")
    print("\n🔗 Quick Start:")
    print("1. Go to https://render.com")
    print("2. Create new Web Service")
    print("3. Connect your GitHub repo")
    print("4. Add your OPENAI_API_KEY")
    print("5. Deploy!")

if __name__ == "__main__":
    main() 