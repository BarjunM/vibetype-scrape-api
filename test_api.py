"""
Test script for Web Content Parser API
"""
import requests
import json
import time


# Sample HTML content for testing
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Climate Change and Environmental Impact</title>
</head>
<body>
    <nav>Navigation menu that should be removed</nav>
    
    <header>
        <h1>Climate Change and Environmental Impact</h1>
    </header>
    
    <main>
        <article>
            <h2>Introduction to Climate Change</h2>
            <p>Climate change refers to long-term shifts in global or regional climate patterns. 
            It is primarily attributed to increased levels of atmospheric carbon dioxide produced 
            by the use of fossil fuels since the mid-20th century.</p>
            
            <h2>Main Causes of Climate Change</h2>
            <p>The primary causes of climate change include:</p>
            <ul>
                <li>Greenhouse gas emissions from burning fossil fuels</li>
                <li>Deforestation and land use changes</li>
                <li>Industrial processes and manufacturing</li>
                <li>Transportation and energy consumption</li>
            </ul>
            
            <h2>Environmental Impacts</h2>
            <p>Climate change has numerous environmental consequences:</p>
            
            <h3>Ocean Effects</h3>
            <p>Rising sea levels, ocean acidification, and changes in ocean currents 
            are major concerns. Marine ecosystems are being disrupted, affecting 
            fish populations and coral reefs worldwide.</p>
            
            <h3>Weather Patterns</h3>
            <p>Extreme weather events are becoming more frequent and severe. 
            This includes stronger hurricanes, prolonged droughts, intense flooding, 
            and unprecedented heatwaves.</p>
            
            <h2>Solutions and Mitigation</h2>
            <p>Addressing climate change requires comprehensive action:</p>
            <ul>
                <li>Transition to renewable energy sources</li>
                <li>Improve energy efficiency in buildings and transportation</li>
                <li>Protect and restore natural ecosystems</li>
                <li>Implement carbon pricing and regulations</li>
            </ul>
            
            <h2>Conclusion</h2>
            <p>Climate change is one of the most pressing challenges of our time. 
            It requires immediate and sustained action from individuals, businesses, 
            and governments worldwide to mitigate its impacts and adapt to changing conditions.</p>
        </article>
    </main>
    
    <footer>Footer content that should be removed</footer>
    
    <script>
        // This script should be removed
        console.log("Analytics tracking");
    </script>
</body>
</html>
"""


def test_api_endpoint(url: str, payload: dict, endpoint: str = "/process"):
    """Test an API endpoint"""
    print(f"\n{'='*50}")
    print(f"Testing {endpoint} endpoint")
    print(f"{'='*50}")
    
    try:
        start_time = time.time()
        response = requests.post(f"{url}{endpoint}", json=payload)
        end_time = time.time()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS")
            print(f"Title: {data.get('title', 'N/A')}")
            print(f"Processing Time: {data.get('processing_time', 0):.2f} seconds")
            print(f"Total Chunks: {len(data.get('chunks', []))}")
            print(f"Relevant Chunks: {len(data.get('most_relevant_chunks', []))}")
            
            # Show first few chunks
            chunks = data.get('chunks', [])
            if chunks:
                print(f"\n📋 Sample Chunks:")
                for i, chunk in enumerate(chunks[:2]):
                    print(f"\nChunk {i+1}: {chunk['title']}")
                    print(f"Type: {chunk['type']}")
                    print(f"Tokens: {chunk['token_count']}")
                    print(f"Content Preview: {chunk['content'][:200]}...")
            
            # Show relevant chunks
            relevant = data.get('most_relevant_chunks', [])
            if relevant:
                print(f"\n🎯 Most Relevant Chunks:")
                for i, chunk in enumerate(relevant):
                    print(f"\n{i+1}. {chunk['title']}")
                    print(f"   Score: {chunk['similarity_score']:.3f}")
                    print(f"   Type: {chunk['type']}")
                    print(f"   Preview: {chunk['content'][:150]}...")
            
            # Show metadata
            metadata = data.get('metadata', {})
            if metadata:
                print(f"\n📊 Metadata:")
                for key, value in metadata.items():
                    print(f"   {key}: {value}")
                    
        else:
            print(f"\n❌ FAILED")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ CONNECTION ERROR")
        print("Make sure the API server is running on the specified URL")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


def test_parse_only_endpoint(url: str, html: str):
    """Test the parse-only endpoint"""
    print(f"\n{'='*50}")
    print(f"Testing /parse-only endpoint")
    print(f"{'='*50}")
    
    try:
        response = requests.post(f"{url}/parse-only", json={"html": html})
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS")
            print(f"Title: {data.get('title', 'N/A')}")
            print(f"Fallback Used: {data.get('fallback_used', False)}")
            print(f"Markdown Length: {len(data.get('clean_markdown', ''))}")
            print(f"Markdown Preview: {data.get('clean_markdown', '')[:300]}...")
        else:
            print(f"\n❌ FAILED")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


def main():
    """Run all tests"""
    api_url = "http://localhost:8000"
    
    print("🚀 Web Content Parser API Test Suite")
    print(f"Testing API at: {api_url}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{api_url}/health")
        if response.status_code == 200:
            print("✅ API is running")
        else:
            print("❌ API health check failed")
            return
    except:
        print("❌ Cannot connect to API. Make sure it's running with: python main.py")
        return
    
    # Test different queries
    test_queries = [
        {
            "query": "What are the main causes of climate change?",
            "description": "Specific question about causes"
        },
        {
            "query": "ocean effects environmental impact",
            "description": "Keywords about ocean impacts"
        },
        {
            "query": "solutions mitigation renewable energy",
            "description": "Keywords about solutions"
        },
        {
            "query": "Summarize the environmental impacts",
            "description": "Summarization request"
        }
    ]
    
    # Test main processing endpoint
    for test in test_queries:
        payload = {
            "html": SAMPLE_HTML,
            "query": test["query"],
            "chunk_size": 500,
            "top_k": 2
        }
        
        print(f"\n🔍 Test: {test['description']}")
        print(f"Query: '{test['query']}'")
        test_api_endpoint(api_url, payload)
        time.sleep(1)  # Brief pause between tests
    
    # Test parse-only endpoint
    test_parse_only_endpoint(api_url, SAMPLE_HTML)
    
    print(f"\n{'='*50}")
    print("🎉 Test suite completed!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
