#!/usr/bin/env python3
"""
Test script for deployed API
"""
import requests
import json
import sys

def test_deployed_api(base_url):
    """Test the deployed API"""
    print(f"🧪 Testing deployed API at: {base_url}")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False
    
    # Test main endpoint
    test_payload = {
        "html": """
        <html>
        <head><title>Test Document</title></head>
        <body>
            <h1>Test Document</h1>
            <p>This is a test document about artificial intelligence.</p>
            <h2>What is AI?</h2>
            <p>Artificial Intelligence is the simulation of human intelligence in machines.</p>
            <h2>Applications</h2>
            <p>AI is used in many fields including healthcare, finance, and transportation.</p>
        </body>
        </html>
        """,
        "query": "What is artificial intelligence?",
        "chunk_size": 500,
        "top_k": 2
    }
    
    try:
        print("🔄 Testing main /process endpoint...")
        response = requests.post(
            f"{base_url}/process", 
            json=test_payload, 
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Main endpoint working")
            print(f"   Title: {data.get('title', 'N/A')}")
            print(f"   Processing time: {data.get('processing_time', 0):.2f}s")
            print(f"   Chunks created: {len(data.get('chunks', []))}")
            print(f"   Relevant chunks: {len(data.get('most_relevant_chunks', []))}")
            
            # Show first relevant chunk
            relevant = data.get('most_relevant_chunks', [])
            if relevant:
                print(f"   Top result: {relevant[0]['title']}")
                print(f"   Similarity score: {relevant[0]['similarity_score']:.3f}")
            
            return True
        else:
            print(f"❌ Main endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing main endpoint: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python test_deployment.py <your-api-url>")
        print("Example: python test_deployment.py https://your-app.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    if test_deployed_api(base_url):
        print("\n🎉 API is working correctly!")
        print(f"📚 API Documentation: {base_url}/docs")
        print(f"🔍 Interactive docs: {base_url}/redoc")
    else:
        print("\n❌ API test failed. Check your deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main() 