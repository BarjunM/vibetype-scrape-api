# Deployment Guide for Web Content Parser API

This guide will help you deploy your API to various hosting platforms. Choose the option that best fits your needs.

## Prerequisites

1. **OpenAI API Key**: You'll need an OpenAI API key for the semantic search functionality
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## Option 1: Railway (Recommended - Easiest)

### Step 1: Sign Up
1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account

### Step 2: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway will automatically detect it's a Python app

### Step 3: Configure Environment Variables
1. Go to your project dashboard
2. Click on "Variables" tab
3. Add your environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Step 4: Deploy
1. Railway will automatically deploy your app
2. Your API will be available at: `https://your-app-name.railway.app`

## Option 2: Render (Free Tier Available)

### Step 1: Sign Up
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account

### Step 2: Deploy
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `vibetype-scrape-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Configure Environment Variables
1. In your service settings, go to "Environment"
2. Add your environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Step 4: Deploy
1. Click "Create Web Service"
2. Your API will be available at: `https://your-app-name.onrender.com`

## Option 3: Heroku

### Step 1: Install Heroku CLI
```bash
# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Or use winget
winget install --id=Heroku.HerokuCLI
```

### Step 2: Login and Deploy
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add your code to Heroku
git add .
git commit -m "Initial deployment"
git push heroku main

# Set environment variables
heroku config:set OPENAI_API_KEY=your_openai_api_key_here

# Open your app
heroku open
```

## Option 4: Google Cloud Run (Serverless)

### Step 1: Install Google Cloud CLI
```bash
# Download from: https://cloud.google.com/sdk/docs/install
```

### Step 2: Setup and Deploy
```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy vibetype-scrape-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_openai_api_key_here
```

## Option 5: DigitalOcean App Platform

### Step 1: Create App
1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository

### Step 2: Configure
1. Select "Python" as the environment
2. Set build command: `pip install -r requirements.txt`
3. Set run command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables
1. Add your `OPENAI_API_KEY` in the environment variables section

### Step 4: Deploy
1. Click "Create Resources"
2. Your API will be available at the provided URL

## Testing Your Deployed API

Once deployed, test your API using the provided test script:

```bash
# Update the URL in test_api.py to your deployed URL
python test_api.py
```

Or test manually with curl:

```bash
curl -X POST "https://your-app-url.com/process" \
     -H "Content-Type: application/json" \
     -d '{
       "html": "<html><body><h1>Test</h1><p>This is a test.</p></body></html>",
       "query": "What is this about?"
     }'
```

## Environment Variables

Make sure to set these environment variables on your hosting platform:

- `OPENAI_API_KEY`: Your OpenAI API key (required for semantic search)
- `EMBEDDING_MODEL`: Optional, defaults to `text-embedding-3-small`
- `API_HOST`: Optional, defaults to `0.0.0.0`
- `API_PORT`: Optional, defaults to `8000` (set by hosting platform)

## Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **Port Issues**: Most platforms set `$PORT` environment variable automatically
3. **Memory Issues**: If you get memory errors, consider upgrading your plan
4. **Cold Starts**: Render free tier has cold starts - first request may be slow

### Debugging:

1. Check your platform's logs for error messages
2. Test locally first: `python main.py`
3. Verify your OpenAI API key is working
4. Check that all files are committed to your repository

## Cost Considerations

- **Railway**: $5/month after free tier
- **Render**: Free tier available, then $7/month
- **Heroku**: $7/month minimum
- **Google Cloud Run**: Pay-per-use (very cheap for low traffic)
- **DigitalOcean**: $5/month minimum

## Security Notes

1. Never commit your API keys to version control
2. Use environment variables for sensitive data
3. Consider adding rate limiting for production use
4. Monitor your OpenAI API usage to control costs

## Next Steps

After deployment:
1. Test all endpoints thoroughly
2. Set up monitoring and logging
3. Consider adding authentication if needed
4. Set up a custom domain if desired
5. Configure automatic deployments from your Git repository 