"""
Simple example of using the Web Content Parser API
"""
import os
from html_parser import HTMLParser
from content_chunker import ContentChunker


def example_local_usage():
    """Example of using the components locally without the API"""
    
    # Sample HTML content
    sample_html = """
    <html>
    <head><title>Python Programming Guide</title></head>
    <body>
        <nav>Skip this navigation</nav>
        <main>
            <h1>Introduction to Python Programming</h1>
            <p>Python is a high-level, interpreted programming language known for its simplicity and readability.</p>
            
            <h2>Key Features</h2>
            <p>Python offers several advantages:</p>
            <ul>
                <li>Easy to learn and use</li>
                <li>Extensive standard library</li>
                <li>Cross-platform compatibility</li>
                <li>Strong community support</li>
            </ul>
            
            <h2>Common Use Cases</h2>
            <h3>Web Development</h3>
            <p>Python is widely used for web development with frameworks like Django and Flask.</p>
            
            <h3>Data Science</h3>
            <p>Python excels in data analysis, machine learning, and scientific computing with libraries like pandas, NumPy, and scikit-learn.</p>
            
            <h2>Getting Started</h2>
            <p>To begin programming in Python, you need to install Python from python.org and choose a code editor or IDE.</p>
        </main>
        <footer>Footer content to ignore</footer>
    </body>
    </html>
    """
    
    print("🐍 Web Content Parser - Local Usage Example")
    print("="*50)
    
    # Step 1: Parse HTML
    print("\n1. Parsing HTML content...")
    parser = HTMLParser()
    result = parser.extract_main_content(sample_html)
    
    if result["success"]:
        print(f"✅ Successfully extracted content")
        print(f"Title: {result['title']}")
        print(f"Markdown length: {len(result['markdown'])} characters")
        
        # Step 2: Create chunks
        print("\n2. Creating content chunks...")
        chunker = ContentChunker(target_chunk_size=500)
        chunks = chunker.chunk_by_headings(result['markdown'], result['title'])
        
        print(f"✅ Created {len(chunks)} chunks")
        
        # Display chunks
        print("\n3. Content Chunks:")
        print("-" * 40)
        
        for i, chunk in enumerate(chunks, 1):
            print(f"\nChunk {i}: {chunk['title']}")
            print(f"Type: {chunk['type']}")
            print(f"Tokens: {chunk['token_count']}")
            print(f"Content preview: {chunk['content'][:150]}...")
            print("-" * 40)
        
        # Step 3: Simple keyword search (without OpenAI)
        print("\n4. Simple keyword search example:")
        query = "web development frameworks"
        print(f"Query: '{query}'")
        
        # Simple keyword matching
        query_words = set(query.lower().split())
        scored_chunks = []
        
        for chunk in chunks:
            content = f"{chunk['title']} {chunk['content']}".lower()
            content_words = set(content.split())
            
            common_words = query_words.intersection(content_words)
            score = len(common_words) / len(query_words) if query_words else 0
            
            if score > 0:
                scored_chunks.append((chunk, score))
        
        # Sort by relevance
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n🎯 Top relevant chunks:")
        for chunk, score in scored_chunks[:2]:
            print(f"\nTitle: {chunk['title']}")
            print(f"Relevance Score: {score:.2f}")
            print(f"Content: {chunk['content'][:200]}...")
    
    else:
        print(f"❌ Failed to parse HTML: {result.get('error', 'Unknown error')}")


def api_usage_example():
    """Example of how to use the API programmatically"""
    
    print("\n" + "="*50)
    print("📡 API Usage Example")
    print("="*50)
    
    api_code = '''
import requests
import json

# API endpoint
url = "http://localhost:8000/process"

# Sample request
payload = {
    "html": "<html><body><h1>Article Title</h1><p>Content here...</p></body></html>",
    "query": "What is this article about?",
    "chunk_size": 750,
    "top_k": 3
}

# Make request
response = requests.post(url, json=payload)

if response.status_code == 200:
    result = response.json()
    print(f"Title: {result['title']}")
    print(f"Total chunks: {len(result['chunks'])}")
    print(f"Relevant chunks: {len(result['most_relevant_chunks'])}")
    
    # Show most relevant content
    for chunk in result['most_relevant_chunks']:
        print(f"\\nRelevant: {chunk['title']}")
        print(f"Score: {chunk['similarity_score']:.3f}")
        print(f"Content: {chunk['content'][:200]}...")
else:
    print(f"Error: {response.status_code} - {response.text}")
'''
    
    print("Here's how to use the API programmatically:")
    print(api_code)
    
    print("\nTo run this example:")
    print("1. Start the API server: python main.py")
    print("2. Run the above code in a separate Python script")
    print("3. Make sure you have set your OPENAI_API_KEY in .env file")


if __name__ == "__main__":
    # Run local example
    example_local_usage()
    
    # Show API example
    api_usage_example()
    
    print("\n" + "="*50)
    print("🚀 Ready to use the Web Content Parser!")
    print("="*50)
    print("\nNext steps:")
    print("1. Set up your OpenAI API key in .env file")
    print("2. Run 'python main.py' to start the API server")
    print("3. Run 'python test_api.py' to test all functionality")
    print("4. Visit http://localhost:8000/docs for interactive API documentation")
