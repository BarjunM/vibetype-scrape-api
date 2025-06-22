#!/usr/bin/env python3
"""
Railway Deployment Helper Script
"""
import os
import subprocess
import sys

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
            subprocess.run(['git', 'commit', '-m', 'Initial commit'])
            print("✅ Git repository initialized")
        else:
            print("✅ Git repository found")
        return True
    except Exception as e:
        print(f"❌ Error checking git repository: {e}")
        return False

def check_railway_cli():
    """Check if Railway CLI is installed"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Railway CLI not found. Installing...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'railway'])
            print("✅ Railway CLI installed")
        else:
            print("✅ Railway CLI found")
        return True
    except FileNotFoundError:
        print("❌ Railway CLI not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'railway'])
        print("✅ Railway CLI installed")
        return True

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

def main():
    """Main deployment helper function"""
    print("🚀 Railway Deployment Helper")
    print("=" * 40)
    
    # Check prerequisites
    if not check_git():
        return
    
    if not check_git_repo():
        return
    
    if not check_railway_cli():
        return
    
    check_env_file()
    
    print("\n📋 Next Steps:")
    print("1. Make sure your code is committed to git")
    print("2. Get your OpenAI API key from: https://platform.openai.com/api-keys")
    print("3. Go to https://railway.app and sign up")
    print("4. Create a new project and connect your GitHub repository")
    print("5. Add your OPENAI_API_KEY as an environment variable")
    print("6. Deploy!")
    
    print("\n🔗 Quick Links:")
    print("- Railway Dashboard: https://railway.app/dashboard")
    print("- OpenAI API Keys: https://platform.openai.com/api-keys")
    print("- Your API Documentation: https://your-app-name.railway.app/docs")

if __name__ == "__main__":
    main() 