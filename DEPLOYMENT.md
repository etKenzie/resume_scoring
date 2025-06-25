# Resume Scoring API - Deployment Guide

This guide covers multiple hosting options for your FastAPI resume scoring application.

## Prerequisites

1. **OpenAI API Key**: You'll need an OpenAI API key for the AI agents
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## Environment Variables

Set these environment variables in your hosting platform:

```bash
OPENAI_API_KEY=your_openai_api_key_here
MODEL_CHOICE=gpt-4-turbo-preview  # Optional, defaults to gpt-4-turbo-preview
```

## Option 1: Railway (Recommended - Easiest)

Railway is perfect for this type of application with automatic deployments and good free tier.

### Steps:
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub repository
4. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `MODEL_CHOICE`: gpt-4-turbo-preview (optional)
5. Railway will automatically detect the Dockerfile and deploy
6. Your API will be available at: `https://your-app-name.railway.app`

### Benefits:
- ✅ Automatic deployments from Git
- ✅ Free tier with 500 hours/month
- ✅ Built-in monitoring
- ✅ Custom domains
- ✅ SSL certificates included

## Option 2: Render

Render is another excellent option with good free tier and easy deployment.

### Steps:
1. Go to [render.com](https://render.com) and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: resume-scoring-api
   - **Environment**: Docker
   - **Region**: Choose closest to your users
   - **Branch**: main
   - **Build Command**: (leave empty, uses Dockerfile)
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Click "Create Web Service"

### Benefits:
- ✅ Free tier with 750 hours/month
- ✅ Automatic deployments
- ✅ Custom domains
- ✅ SSL included

## Option 3: Heroku

Heroku is a classic choice with good reliability.

### Steps:
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your_key_here
   git push heroku main
   ```

### Benefits:
- ✅ Reliable and well-established
- ✅ Good documentation
- ✅ Add-ons ecosystem

## Option 4: DigitalOcean App Platform

For more control and scalability.

### Steps:
1. Go to DigitalOcean App Platform
2. Connect your GitHub repository
3. Configure as Docker app
4. Set environment variables
5. Deploy

### Benefits:
- ✅ More control over infrastructure
- ✅ Better for scaling
- ✅ Global CDN

## Option 5: AWS/GCP/Azure (Enterprise)

For production workloads with high traffic.

### AWS ECS/Fargate:
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker build -t resume-scoring-api .
docker tag resume-scoring-api:latest your-account.dkr.ecr.us-east-1.amazonaws.com/resume-scoring-api:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/resume-scoring-api:latest
```

### Benefits:
- ✅ Maximum scalability
- ✅ Advanced monitoring
- ✅ Enterprise features

## API Usage

Once deployed, your API will be available at:

### Endpoints:
- **Health Check**: `GET /events/health`
- **API Info**: `GET /events/`
- **Score Resume**: `POST /events/score-resume`
- **API Documentation**: `GET /docs`

### Example Usage:

```bash
curl -X POST "https://your-app.railway.app/events/score-resume" \
  -H "Content-Type: multipart/form-data" \
  -F "resume=@resume.pdf" \
  -F "job_description=We are looking for a Python developer with 3+ years experience..." \
  -F "target_skills=Python,JavaScript,React,SQL"
```

### Python Client Example:

```python
import requests

url = "https://your-app.railway.app/events/score-resume"
files = {"resume": open("resume.pdf", "rb")}
data = {
    "job_description": "We are looking for a Python developer...",
    "target_skills": "Python,JavaScript,React,SQL"
}

response = requests.post(url, files=files, data=data)
result = response.json()
print(result)
```

## Monitoring & Maintenance

### Health Checks:
- Your API includes a health check endpoint at `/events/health`
- Most platforms will automatically monitor this endpoint

### Logs:
- Railway: View logs in the dashboard
- Render: Available in the service dashboard
- Heroku: `heroku logs --tail`

### Scaling:
- Start with free tiers
- Upgrade as traffic increases
- Consider adding caching for repeated requests

## Security Considerations

1. **API Keys**: Never commit API keys to Git
2. **Rate Limiting**: Consider adding rate limiting for production
3. **File Validation**: The API validates file types and sizes
4. **HTTPS**: All platforms provide SSL certificates

## Troubleshooting

### Common Issues:

1. **Port Issues**: Make sure your app uses `$PORT` environment variable
2. **Memory Limits**: Free tiers have memory limits (512MB-1GB)
3. **Timeout Issues**: Resume scoring can take 30-60 seconds
4. **File Size**: 10MB limit on uploaded files

### Debug Commands:
```bash
# Test locally
docker build -t resume-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key resume-api

# Check logs
docker logs container_name
```

## Cost Estimation

### Free Tiers:
- **Railway**: $5/month after free tier (500 hours)
- **Render**: $7/month after free tier (750 hours)
- **Heroku**: $7/month for basic dyno

### Production (1000 requests/month):
- **Railway**: ~$10-15/month
- **Render**: ~$15-20/month
- **AWS**: ~$20-30/month (with more features)

Choose based on your expected traffic and budget! 