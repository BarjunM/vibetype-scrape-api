# Deployment Troubleshooting Guide

## Issue: Python 3.13 Compatibility Error

### Problem
```
TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'
```

### Root Cause
This error occurs because:
1. Render is using Python 3.13 by default
2. Older versions of FastAPI (0.88.0) and Pydantic (1.10.2) are incompatible with Python 3.13
3. Python 3.13 introduced breaking changes in the typing system

### Solution Applied
1. **Updated requirements.txt** with compatible versions:
   - FastAPI: 0.88.0 → 0.104.1
   - Pydantic: 1.10.2 → 2.5.0
   - Uvicorn: 0.20.0 → 0.24.0
   - OpenAI: 0.27.0 → 1.3.7

2. **Added missing dependencies**:
   - numpy==1.24.3
   - scikit-learn==1.3.2
   - tiktoken==0.5.2
   - readability-lxml==0.8.1

3. **Specified Python version**:
   - Added `runtime.txt` with `python-3.11.7`
   - Updated `render.yaml` to use Python 3.11.7

## Deployment Steps After Fix

1. **Commit the changes:**
   ```bash
   git add .
   git commit -m "Fix Python 3.13 compatibility issues"
   git push origin main
   ```

2. **Redeploy on Render:**
   - Go to your Render dashboard
   - Click "Manual Deploy" → "Deploy latest commit"

3. **Monitor the build:**
   - Watch the build logs for any new errors
   - The build should now succeed

## Testing the Fix

### Local Testing
```bash
# Test locally first
python main.py
```

### Deployment Testing
```bash
# Test the deployed API
python test_deployment.py https://your-app-name.onrender.com
```

## Common Issues and Solutions

### 1. Build Still Fails
**Check:**
- All files are committed and pushed
- Environment variables are set correctly
- Python version is specified

**Solution:**
- Verify `runtime.txt` exists with `python-3.11.7`
- Check `render.yaml` configuration
- Ensure `requirements.txt` is up to date

### 2. Runtime Errors
**Check:**
- OpenAI API key is set correctly
- All dependencies are installed

**Solution:**
- Verify environment variables in Render dashboard
- Check build logs for missing dependencies

### 3. Cold Start Issues (Render Free)
**Problem:** First request takes 10-30 seconds
**Solution:** 
- This is normal for free tier
- Consider upgrading to paid plan for better performance

### 4. Memory Issues
**Problem:** API runs out of memory
**Solution:**
- Reduce chunk sizes in requests
- Monitor memory usage in Render dashboard
- Consider upgrading plan

## Debug Commands

### Check Python Version
```bash
python --version
```

### Test Dependencies
```bash
pip install -r requirements.txt
python -c "import fastapi; print('FastAPI OK')"
python -c "import openai; print('OpenAI OK')"
```

### Test API Locally
```bash
python main.py
# Then visit http://localhost:8000/health
```

## Environment Variables Checklist

Make sure these are set in Render:
- ✅ `OPENAI_API_KEY`: Your OpenAI API key
- ✅ `PYTHON_VERSION`: 3.11.7 (optional, specified in runtime.txt)

## Support Resources

- **Render Docs:** https://docs.render.com
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **OpenAI Docs:** https://platform.openai.com/docs

## Next Steps After Successful Deployment

1. ✅ Test all endpoints
2. ✅ Set up monitoring
3. ✅ Configure custom domain (optional)
4. ✅ Set up CI/CD for automatic deployments 