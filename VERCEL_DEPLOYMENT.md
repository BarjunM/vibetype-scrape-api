# VibeType Scrape API - Vercel Deployment Guide

This API provides content extraction and semantic search capabilities for the VibeType Chrome extension.

## Deploying to Vercel

### Prerequisites

-   A [Vercel](https://vercel.com) account
-   [Vercel CLI](https://vercel.com/cli) (optional for local development)
-   An OpenAI API key

### Deployment Steps

1. **Set up environment variables on Vercel**:

    - `OPENAI_API_KEY`: Your OpenAI API key

2. **Deploy to Vercel**:

    ```bash
    # Install Vercel CLI (if not already installed)
    npm install -g vercel

    # Login to Vercel
    vercel login

    # Deploy
    vercel
    ```

    Alternatively, you can connect your GitHub repository to Vercel for automatic deployments.

3. **Environment Variables**:
    - Make sure to set your `OPENAI_API_KEY` in the Vercel project settings.

### Local Development

To run the API locally:

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Set up environment variables:

    ```bash
    # Create a .env file with your OpenAI API key
    echo "OPENAI_API_KEY=your_api_key_here" > .env
    ```

3. Run the server:

    ```bash
    cd api
    python index.py
    ```

    The API will be available at `http://localhost:8000`.

## API Endpoints

-   **GET /** - Health check
-   **GET /health** - Detailed health check
-   **POST /process** - Main endpoint to process HTML content and find relevant chunks
-   **POST /parse-only** - Parse HTML without chunking or semantic search

## Project Structure

```plaintext
vibetype-scrape-api/
├── api/
│   └── index.py           # Vercel entry point
├── content_chunker.py     # Content chunking functionality
├── html_parser.py         # HTML parsing functionality
├── main.py                # Main FastAPI application
├── requirements.txt       # Python dependencies
├── semantic_search.py     # Semantic search functionality
└── vercel.json            # Vercel configuration
```
