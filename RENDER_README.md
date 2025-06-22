# Render Deployment Guide for Web Content Parser API

This guide will help you deploy your Web Content Parser API to Render.com.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the deployment helper
python render_deploy.py
```

### Option 2: Manual Setup
Follow the step-by-step instructions below.

## 📋 Prerequisites

1. **GitHub Account**: Your code must be in a GitHub repository
2. **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)
3. **Render Account**: Sign up at [render.com](https://render.com)

## 🔧 Step-by-Step Deployment

### Step 1: Prepare Your Code

1. **Ensure your code is committed to git:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Verify required files exist:**
   - ✅ `main.py` (FastAPI application)
   - ✅ `requirements.txt` (Python dependencies)
   - ✅ `render.yaml` (Render configuration)

### Step 2: Sign Up for Render

1. Go to [render.com](https://render.com)
2. Click "Get Started"
3. Sign up with your GitHub account
4. Verify your email address

### Step 3: Create Web Service

1. In your Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository (`vibetype-scrape-api`)

### Step 4: Configure the Service

Use these exact settings:

| Setting | Value |
|---------|-------|
| **Name** | `vibetype-scrape-api` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` (or choose paid plan) |

### Step 5: Add Environment Variables

1. Click on **"Environment"** tab
2. Add the following environment variable:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `your_actual_openai_api_key_here` |

⚠️ **Important**: Replace `your_actual_openai_api_key_here` with your real OpenAI API key.

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Wait for the build to complete (2-5 minutes)
3. Your API will be available at: `https://your-app-name.onrender.com`

## 🧪 Testing Your Deployment

### Option 1: Use the Test Script
```bash
python test_deployment.py https://your-app-name.onrender.com
```

### Option 2: Manual Testing
```bash
# Test health endpoint
curl https://your-app-name.onrender.com/health

# Test main endpoint
curl -X POST "https://your-app-name.onrender.com/process" \
     -H "Content-Type: application/json" \
     -d '{
       "html": "<html><body><h1>Test</h1><p>This is a test.</p></body></html>",
       "query": "What is this about?"
     }'
```

### Option 3: Check API Documentation
Visit: `https://your-app-name.onrender.com/docs`

## 📊 API Endpoints

Your deployed API will have these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Detailed health status |
| `/process` | POST | Main content processing |
| `/parse-only` | POST | HTML parsing only |
| `/docs` | GET | Interactive API documentation |
| `/redoc` | GET | Alternative API documentation |

## 🔍 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check that all dependencies are in `requirements.txt`
   - Verify Python version compatibility
   - Check build logs in Render dashboard

2. **API Not Responding**
   - Check if service is running in Render dashboard
   - Verify environment variables are set correctly
   - Check logs for error messages

3. **OpenAI API Errors**
   - Verify your API key is correct
   - Check your OpenAI account has credits
   - Ensure the API key is set in environment variables

4. **Cold Start Issues**
   - Free tier has cold starts (first request may be slow)
   - Consider upgrading to paid plan for better performance

### Debugging Steps

1. **Check Render Logs:**
   - Go to your service in Render dashboard
   - Click "Logs" tab
   - Look for error messages

2. **Test Locally First:**
   ```bash
   python main.py
   # Then test at http://localhost:8000
   ```

3. **Verify Environment Variables:**
   - Check Render dashboard → Environment tab
   - Ensure `OPENAI_API_KEY` is set correctly

## 💰 Cost Considerations

- **Free Tier**: 
  - 750 hours/month
  - Cold starts (slower first request)
  - Sleeps after 15 minutes of inactivity
- **Paid Plans**: 
  - Starting at $7/month
  - No cold starts
  - Always running

## 🔒 Security Notes

1. **Never commit API keys** to your repository
2. **Use environment variables** for sensitive data
3. **Monitor your OpenAI usage** to control costs
4. **Consider adding authentication** for production use

## 📈 Monitoring

### Render Dashboard
- Monitor service status
- View logs and errors
- Check resource usage

### OpenAI Usage
- Monitor API usage at [OpenAI Platform](https://platform.openai.com/usage)
- Set up billing alerts

## 🚀 Next Steps

After successful deployment:

1. **Set up monitoring** and alerts
2. **Add rate limiting** if needed
3. **Configure custom domain** (optional)
4. **Set up automatic deployments** from GitHub
5. **Add authentication** for production use

## 🔗 Useful Links

- [Render Dashboard](https://dashboard.render.com)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Render Documentation](https://render.com/docs)

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Render logs in the dashboard
3. Check [Render Community](https://community.render.com)
4. Contact Render support if needed

---

**Happy Deploying! 🎉** 