#!/usr/bin/env python3
"""
Test script for deployed API
"""
import requests
import json
import sys
from typing import Optional


def test_api_endpoint(base_url: str, endpoint: str = "/health") -> bool:
    """Test a simple endpoint"""
    try:
        response = requests.get(f"{base_url}{endpoint}", timeout=10)
        if response.status_code == 200:
            print(f"✅ {endpoint} - OK")
            return True
        else:
            print(f"❌ {endpoint} - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {endpoint} - Error: {e}")
        return False


def test_process_endpoint(base_url: str) -> bool:
    """Test the main process endpoint"""
    test_html = """
    <html>
        <head><title>Test Article</title></head>
        <body>
            <h1>Climate Change</h1>
            <p>Climate change is a significant challenge facing our planet.</p>
            <h2>Effects</h2>
            <p>Rising temperatures and sea levels are major concerns.</p>
        </body>
    </html>
    """
    
    test_data = {
        "html": test_html,
        "query": "What are the effects of climate change?",
        "chunk_size": 500,
        "top_k": 2
    }
    
    try:
        response = requests.post(
            f"{base_url}/process",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ /process - OK")
                print(f"   Title: {result.get('title', 'N/A')}")
                print(f"   Chunks: {len(result.get('chunks', []))}")
                print(f"   Relevant chunks: {len(result.get('most_relevant_chunks', []))}")
                return True
            else:
                print("❌ /process - API returned success=False")
                return False
        else:
            print(f"❌ /process - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ /process - Error: {e}")
        return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python test_deployment.py <base_url>")
        print("Example: python test_deployment.py https://your-app.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    print(f"Testing API at: {base_url}")
    print("=" * 50)
    
    # Test basic endpoints
    health_ok = test_api_endpoint(base_url, "/health")
    root_ok = test_api_endpoint(base_url, "/")
    
    # Test main functionality
    process_ok = test_process_endpoint(base_url)
    
    print("=" * 50)
    if health_ok and root_ok and process_ok:
        print("🎉 All tests passed! Your API is working correctly.")
        print(f"📖 API Documentation: {base_url}/docs")
        print(f"🔗 Health Check: {base_url}/health")
    else:
        print("❌ Some tests failed. Check your deployment.")
        sys.exit(1)


if __name__ == "__main__":
    main() 