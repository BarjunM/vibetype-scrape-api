# API Deployment Guide

This guide covers multiple hosting options for your Web Content Parser & QA Assistant API.

## 🚀 Quick Start - Render (Recommended)

### Step 1: Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name:** `vibetype-scrape-api`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

5. Add Environment Variables:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** Your OpenAI API key

6. Click "Create Web Service"

### Step 3: Test Your Deployment
```bash
python test_deployment.py https://your-app-name.onrender.com
```

## 🌐 Alternative Hosting Options

### Railway (Fast & Reliable)
**Cost:** $5/month (no free tier)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy!

### Heroku (Classic Choice)
**Cost:** $7/month (no free tier)

1. Install Heroku CLI
2. Create app: `heroku create your-app-name`
3. Set environment variable: `heroku config:set OPENAI_API_KEY=your_key`
4. Deploy: `git push heroku main`

### DigitalOcean App Platform
**Cost:** $5/month (no free tier)

1. Go to [digitalocean.com](https://digitalocean.com)
2. Create App Platform
3. Connect GitHub repository
4. Configure Python environment
5. Add environment variables
6. Deploy!

### Google Cloud Run (Most Scalable)
**Cost:** Pay-per-use

1. Install Google Cloud CLI
2. Create project and enable Cloud Run
3. Build and deploy:
```bash
gcloud run deploy vibetype-scrape-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key
```

## 🔧 Environment Variables

All deployments require:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional:
- `EMBEDDING_MODEL`: Defaults to `text-embedding-3-small`
- `API_HOST`: Defaults to `0.0.0.0`
- `API_PORT`: Defaults to `8000` (Render uses `$PORT`)

## 📊 Performance Considerations

### Free Tier Limitations
- **Render Free:** Sleeps after 15 min inactivity, 750 hours/month
- **Railway:** No free tier, $5/month
- **Heroku:** No free tier, $7/month

### Scaling Options
- **Render:** Upgrade to paid plan ($7/month)
- **Railway:** Automatic scaling included
- **Google Cloud Run:** Automatic scaling, pay-per-use

## 🧪 Testing Your Deployment

### Automated Testing
```bash
python test_deployment.py https://your-app-url.com
```

### Manual Testing
```bash
# Health check
curl https://your-app-url.com/health

# Process content
curl -X POST https://your-app-url.com/process \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<h1>Test</h1><p>This is a test.</p>",
    "query": "What is this about?",
    "chunk_size": 500,
    "top_k": 2
  }'
```

### API Documentation
Visit `https://your-app-url.com/docs` for interactive API documentation.

## 🔒 Security Considerations

1. **API Key Security:**
   - Never commit API keys to git
   - Use environment variables
   - Rotate keys regularly

2. **Rate Limiting:**
   - Consider adding rate limiting for production
   - Monitor OpenAI API usage

3. **CORS:**
   - Configure CORS for your frontend domain
   - Current setup allows all origins (development only)

## 📈 Monitoring & Logs

### Render
- View logs in Render dashboard
- Set up alerts for errors

### Railway
- Real-time logs in dashboard
- Built-in monitoring

### Heroku
```bash
heroku logs --tail
```

## 🚨 Troubleshooting

### Common Issues

1. **Build Fails:**
   - Check Python version compatibility
   - Verify all dependencies in requirements.txt

2. **Runtime Errors:**
   - Check environment variables
   - Verify OpenAI API key is valid

3. **Cold Starts (Render Free):**
   - First request may take 10-30 seconds
   - Consider upgrading to paid plan

4. **Memory Issues:**
   - Monitor memory usage
   - Optimize chunk sizes if needed

### Debug Commands
```bash
# Test locally first
python main.py

# Check dependencies
pip list

# Test OpenAI connection
python -c "import openai; print('OpenAI OK')"
```

## 📞 Support

- **Render:** [docs.render.com](https://docs.render.com)
- **Railway:** [docs.railway.app](https://docs.railway.app)
- **Heroku:** [devcenter.heroku.com](https://devcenter.heroku.com)
- **OpenAI:** [platform.openai.com](https://platform.openai.com)

## 🎯 Next Steps

1. Deploy to your chosen platform
2. Test the deployment
3. Set up monitoring
4. Configure custom domain (optional)
5. Set up CI/CD for automatic deployments 