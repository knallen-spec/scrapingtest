# Deployment Guide - Google Maps Company Scraper

This guide covers deploying the Streamlit web application to various cloud platforms.

## Table of Contents
1. [Streamlit Cloud (Recommended - Free)](#streamlit-cloud)
2. [Railway](#railway)
3. [Render](#render)
4. [Heroku](#heroku)
5. [Local Testing](#local-testing)

---

## Streamlit Cloud (Recommended - Free)

Streamlit Cloud is the easiest and FREE option for deploying Streamlit apps.

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository

### Step-by-Step Deployment

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Streamlit web interface"
   git push origin main
   ```

2. **Sign up for Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"

3. **Configure your app**
   - Repository: Select your GitHub repository
   - Branch: `main` (or your branch name)
   - Main file path: `app.py`
   - Click "Deploy!"

4. **Wait for deployment**
   - Streamlit Cloud will install dependencies from `requirements.txt`
   - System packages from `packages.txt` will be installed
   - Playwright browsers will be installed automatically
   - First deployment takes 5-10 minutes

5. **Access your app**
   - Your app will be available at: `https://[your-app-name].streamlit.app`
   - Share this URL with anyone!

### Important Notes for Streamlit Cloud
- **Free tier limits**:
  - 1 GB RAM
  - Limited to 3 apps
  - Apps sleep after inactivity (wake up on access)
- **Browser automation**: Works well with headless mode
- **Secrets management**: Use Streamlit's secrets.toml for sensitive data

---

## Railway

Railway is a modern platform with generous free tier.

### Step-by-Step Deployment

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository

3. **Configure deployment**
   - Railway will auto-detect the `Procfile`
   - Add environment variables if needed:
     - `PORT`: Auto-configured by Railway

4. **Add build command**
   - Settings → Build Command: `pip install -r requirements.txt && playwright install chromium`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

5. **Deploy**
   - Click "Deploy"
   - Your app will be available at the Railway-provided URL

### Railway Pricing
- Free tier: $5 credit/month
- Good for testing and moderate use

---

## Render

Render offers a robust free tier for web applications.

### Step-by-Step Deployment

1. **Create Render account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create new Web Service**
   - Dashboard → "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure service**
   - Name: `google-maps-scraper`
   - Environment: `Python 3`
   - Build Command:
     ```bash
     pip install -r requirements.txt && playwright install-deps && playwright install chromium
     ```
   - Start Command:
     ```bash
     streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
     ```

4. **Advanced settings**
   - Instance Type: Free
   - Environment Variables: None required

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (5-10 minutes)

### Render Free Tier
- 750 hours/month
- Spins down after 15 minutes of inactivity
- Takes ~30 seconds to wake up

---

## Heroku

Heroku is a mature platform with straightforward deployment.

### Prerequisites
- Heroku account
- Heroku CLI installed

### Step-by-Step Deployment

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Windows
   # Download from heroku.com/cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Add buildpacks**
   ```bash
   heroku buildpacks:add --index 1 heroku/python
   heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt
   ```

5. **Create Aptfile** (if not exists)
   - Already created as `packages.txt`

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **Open app**
   ```bash
   heroku open
   ```

### Heroku Pricing
- Free tier discontinued
- Eco dyno: $5/month
- Basic dyno: $7/month

---

## Local Testing

Before deploying to cloud, test locally:

### 1. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Access the app
- Open browser to: `http://localhost:8501`

### 4. Test features
- Fill in search parameters
- Start scraping
- Edit results
- Download CSV

---

## Troubleshooting

### Common Issues

#### 1. Playwright browser not installing
**Solution**: Add this to your deployment configuration:
```bash
playwright install-deps
playwright install chromium
```

#### 2. App crashes during scraping
**Cause**: Insufficient memory
**Solution**:
- Reduce `max_results` limit in the app
- Upgrade to paid tier with more RAM

#### 3. Slow performance
**Cause**: Free tier limitations
**Solution**:
- Use headless mode (enabled by default)
- Scrape smaller batches
- Consider upgrading to paid tier

#### 4. Port binding errors
**Solution**: Make sure start command includes:
```bash
--server.port=$PORT --server.address=0.0.0.0
```

#### 5. CORS errors
**Solution**: Check `.streamlit/config.toml`:
```toml
[server]
enableCORS = false
```

---

## Recommended Platform Comparison

| Platform | Free Tier | Ease of Use | Performance | Best For |
|----------|-----------|-------------|-------------|----------|
| **Streamlit Cloud** | ✅ Yes | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Personal projects, demos |
| **Railway** | 💰 $5/month credit | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Small business, testing |
| **Render** | ✅ Yes (limited) | ⭐⭐⭐⭐ | ⭐⭐⭐ | Side projects |
| **Heroku** | ❌ No | ⭐⭐⭐ | ⭐⭐⭐⭐ | Production apps |

---

## Best Practices

1. **Always use headless mode** in production
2. **Set reasonable limits** on max_results to avoid timeouts
3. **Monitor usage** to stay within free tier limits
4. **Use environment variables** for configuration
5. **Enable error tracking** for production apps
6. **Regular backups** of scraped data

---

## Getting Help

If you encounter issues:
1. Check the platform's documentation
2. Review deployment logs
3. Test locally first
4. Check GitHub Issues for common problems

---

## Next Steps

After deployment:
1. Test all features thoroughly
2. Share the URL with your team
3. Monitor performance and errors
4. Consider upgrading if you need more resources
5. Set up automated backups for your data

Happy scraping! 🚀
