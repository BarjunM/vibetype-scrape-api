# Web Content Parser & QA Assistant

A powerful MVP API that extracts, processes, and semantically searches web content. This tool converts raw HTML into clean markdown, intelligently chunks the content, and uses semantic search to find the most relevant sections based on user queries.

## 🎯 Features

-   **HTML Content Extraction**: Uses readability algorithms to extract main article content
-   **Clean Markdown Conversion**: Converts HTML to well-formatted markdown
-   **Intelligent Chunking**: Splits content by headings or fixed token sizes with overlap
-   **Semantic Search**: Uses OpenAI embeddings to find most relevant content chunks
-   **Fallback Mechanisms**: Graceful degradation when components fail
-   **RESTful API**: Clean FastAPI interface with comprehensive error handling

## 🚀 Quick Start

### Prerequisites

-   Python 3.8+
-   OpenAI API Key (for semantic search functionality)

### Installation

1. **Clone and navigate to the project:**

    ```bash
    cd vibetype-scrape-api
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    ```bash
    # Copy the example environment file
    copy .env.example .env

    # Edit .env and add your OpenAI API key
    OPENAI_API_KEY=your_openai_api_key_here
    ```

4. **Run the API server:**

    ```bash
    python main.py
    ```

    The API will be available at `http://localhost:8000`

### Quick Test

Run the test script to see the API in action:

```bash
python test_api.py
```

## 📖 API Documentation

### Main Endpoint: `/process`

**POST** `/process`

Processes HTML content and returns cleaned markdown with semantic search results.

#### Request Body

```json
{
    "html": "<html>Raw HTML content from document.body.innerHTML</html>",
    "query": "What are the main points about climate change?",
    "chunk_size": 750, // Optional: target chunk size in tokens (100-2000)
    "top_k": 3 // Optional: number of relevant chunks to return (1-10)
}
```

#### Response

```json
{
    "success": true,
    "title": "Article Title",
    "clean_markdown": "# Clean markdown content...",
    "chunks": [
        {
            "id": "1",
            "title": "Section Title",
            "content": "Chunk content...",
            "token_count": 456,
            "type": "heading_based"
        }
    ],
    "most_relevant_chunks": [
        {
            "id": "1",
            "title": "Most Relevant Section",
            "content": "Relevant content...",
            "similarity_score": 0.892,
            "token_count": 456,
            "type": "heading_based"
        }
    ],
    "processing_time": 2.34,
    "metadata": {
        "total_chunks": 5,
        "original_html_length": 15420,
        "markdown_length": 3240,
        "fallback_used": false,
        "search_type": "semantic"
    }
}
```

### Additional Endpoints

#### Health Check: `/health`

**GET** `/health`

Returns API health status.

#### Parse Only: `/parse-only`

**POST** `/parse-only`

Extracts and cleans HTML without chunking or semantic search.

Request body: Raw HTML string

```json
"<html>Raw HTML content</html>"
```

## 🏗️ Architecture

### Core Components

1. **HTMLParser** (`html_parser.py`)

    - Uses `readability-lxml` for main content extraction
    - Converts HTML to markdown with `html2text`
    - Includes fallback cleaning for problematic HTML

2. **ContentChunker** (`content_chunker.py`)

    - Smart chunking by headings (##, ###, etc.)
    - Fixed-size chunking with configurable overlap
    - Token counting using `tiktoken`

3. **SemanticSearcher** (`semantic_search.py`)

    - OpenAI embeddings for semantic similarity
    - Batch processing for efficiency
    - Keyword fallback when embeddings fail

4. **FastAPI Server** (`main.py`)
    - RESTful API with comprehensive error handling
    - Request/response validation with Pydantic
    - Async support for better performance

### Processing Flow

```
Raw HTML → Content Extraction → Markdown Conversion → Chunking → Embedding → Semantic Search → Results
```

## 🔧 Configuration

### Environment Variables

-   `OPENAI_API_KEY`: Required for semantic search
-   `EMBEDDING_MODEL`: Optional, defaults to `text-embedding-3-small`
-   `API_HOST`: Optional, defaults to `0.0.0.0`
-   `API_PORT`: Optional, defaults to `8000`

### Chunking Parameters

-   **Default chunk size**: 750 tokens
-   **Default overlap**: 15%
-   **Supported range**: 100-2000 tokens per chunk

## 🧪 Testing

### Automated Tests

```bash
python test_api.py
```

### Manual Testing with cURL

1. **Process content:**

```bash
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{
       "html": "<html><body><h1>Test</h1><p>Content here</p></body></html>",
       "query": "What is this about?"
     }'
```

2. **Health check:**

```bash
curl "http://localhost:8000/health"
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation.

## 🎯 Use Cases

### Content Summarization

```json
{
    "html": "...",
    "query": "Summarize the main points"
}
```

### Specific Information Extraction

```json
{
    "html": "...",
    "query": "What does this say about pricing?"
}
```

### Content Filtering

```json
{
    "html": "...",
    "query": "Remove advertisements and promotional content"
}
```

### Research Assistance

```json
{
    "html": "...",
    "query": "Find information about methodology and results"
}
```

## 🚦 Error Handling

The API includes comprehensive error handling:

-   **400 Bad Request**: Invalid HTML or processing failures
-   **500 Internal Server Error**: Unexpected server errors
-   **Graceful Degradation**: Falls back to keyword search if semantic search fails

## 📊 Performance Considerations

-   **Chunk Size**: Larger chunks = fewer API calls but less granular search
-   **Overlap**: More overlap = better context but increased processing time
-   **Top-K**: More results = comprehensive but potentially noisy responses

### Typical Performance

-   **Small articles** (< 5KB): ~1-2 seconds
-   **Medium articles** (5-20KB): ~2-5 seconds
-   **Large articles** (> 20KB): ~5-10 seconds

## 🔒 Security Notes

-   Store OpenAI API keys securely
-   Consider rate limiting for production use
-   Validate and sanitize HTML input
-   Monitor API usage and costs

## 🛠️ Development

### Adding New Features

1. **Custom Chunking Strategies**: Modify `ContentChunker`
2. **Alternative Embeddings**: Update `SemanticSearcher`
3. **Content Filters**: Enhance `HTMLParser`
4. **Output Formats**: Extend response models

### Dependencies

-   `fastapi`: Web framework
-   `readability-lxml`: Content extraction
-   `html2text`: HTML to markdown conversion
-   `tiktoken`: Token counting
-   `openai`: Embeddings API
-   `scikit-learn`: Similarity calculations

## 📈 Future Enhancements

-   [ ] Support for multiple embedding models
-   [ ] Content caching for repeated requests
-   [ ] Batch processing endpoint
-   [ ] Custom chunking strategies
-   [ ] Integration with vector databases
-   [ ] Multi-language support
-   [ ] Content quality scoring

## 🐛 Troubleshooting

### Common Issues

1. **"Import could not be resolved"**: Install requirements with `pip install -r requirements.txt`
2. **OpenAI API errors**: Check API key and account credits
3. **HTML parsing fails**: Some pages may require custom handling
4. **Memory issues**: Reduce chunk size or implement pagination

### Getting Help

-   Check the `/health` endpoint for API status
-   Review error messages in API responses
-   Enable debug logging for detailed troubleshooting

## 📄 License

This project is provided as-is for educational and development purposes.

---

**Built with ❤️ using FastAPI, OpenAI, and modern Python tools.**
