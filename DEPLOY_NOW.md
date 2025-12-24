# 🚀 Deploy Your Scraper to the Cloud - Step by Step

Follow these exact steps to get your Google Maps scraper live on the internet in **under 10 minutes**!

---

## ✅ Pre-Deployment Checklist

Before we start, make sure you have:

- [x] GitHub account (you have one since this code is on GitHub)
- [x] Code is committed and pushed (✓ Done!)
- [x] All required files present (✓ Done!)

**You're ready to deploy!** 🎉

---

## 🌐 Streamlit Cloud Deployment (FREE & Easiest)

### Step 1: Access Your GitHub Repository

1. Go to your GitHub repository:
   - **Repository**: `knallen-spec/scrapingtest`
   - **Branch**: `claude/location-company-scraper-s3kNW`

2. **Important**: Make sure the repository is **public** or you have a paid Streamlit Cloud account
   - To make it public: Go to Settings → Change visibility → Make public

### Step 2: Sign Up for Streamlit Cloud

1. **Visit**: [share.streamlit.io](https://share.streamlit.io)

2. **Click**: "Sign up" or "Continue with GitHub"

3. **Authorize**: Allow Streamlit to access your GitHub repositories

4. You'll be redirected to your Streamlit Cloud dashboard

### Step 3: Deploy Your App

1. **Click** the "New app" button (top right)

2. **Fill in the form**:
   ```
   Repository: knallen-spec/scrapingtest
   Branch: claude/location-company-scraper-s3kNW
   Main file path: app.py
   ```

3. **Advanced settings** (Optional - click "Advanced settings" if you want to customize):
   - App URL: Choose a custom subdomain (e.g., `my-scraper.streamlit.app`)
   - Python version: 3.11 (should auto-detect from runtime.txt)

4. **Click** "Deploy!"

### Step 4: Wait for Deployment

The deployment process will:

1. **Clone your repository** (30 seconds)
2. **Install Python dependencies** from requirements.txt (2-3 minutes)
   - playwright
   - pandas
   - streamlit
3. **Install system packages** from packages.txt (2-3 minutes)
   - Browser dependencies
4. **Install Playwright browser** (2-4 minutes)
   - Chromium download and setup
5. **Start the app** (30 seconds)

**Total time**: 5-10 minutes

You'll see a progress log showing each step.

### Step 5: Access Your Live App!

Once deployment is complete:

1. Your app will be available at:
   ```
   https://[your-app-name].streamlit.app
   ```

2. **Bookmark this URL** - this is your live scraper!

3. **Share it** with anyone who needs to use it

---

## 🎯 Using Your Deployed App

Once it's live, here's how to use it:

1. **Open the URL** in any browser

2. **Fill in the sidebar**:
   - Country: e.g., "USA"
   - City: e.g., "New York"
   - Industry: e.g., "restaurants"
   - Max Results: e.g., 50

3. **Click** "🚀 Start Scraping"

4. **Wait** for results (progress bar will show)

5. **Edit** results in the table if needed

6. **Download** CSV by clicking "📥 Download CSV"

---

## ⚠️ Important Notes

### Free Tier Limitations

Streamlit Cloud free tier includes:
- ✅ **1 GB RAM** - Good for scraping up to 100 results at a time
- ✅ **Unlimited users** - Anyone can access your app
- ✅ **Public apps** - Free tier requires public GitHub repos
- ⚠️ **Apps sleep after inactivity** - First load after sleep takes ~30 seconds
- ⚠️ **Up to 3 apps** on free tier

### Recommendations

1. **Start with small batches**:
   - Try max 20-50 results first
   - Scale up if it works smoothly

2. **Use headless mode** (enabled by default)
   - Required for cloud deployment

3. **If app crashes during scraping**:
   - Reduce max_results
   - The free tier might have memory limits
   - Consider upgrading to paid tier ($20/month for more resources)

---

## 🔧 Troubleshooting

### Problem: Deployment fails during Playwright installation

**Solution**:
- Check the deployment logs
- Make sure `packages.txt` is in the root directory
- Verify `requirements.txt` includes playwright

### Problem: App loads but crashes when scraping

**Cause**: Out of memory
**Solution**:
- Reduce max_results to 20-30
- Use headless mode (already enabled)
- Upgrade to paid tier for more RAM

### Problem: "App is not responding"

**Cause**: App went to sleep (free tier behavior)
**Solution**:
- Just refresh the page
- App will wake up in ~30 seconds

### Problem: Can't find the repository

**Solution**:
- Make sure repository is public
- Re-authorize Streamlit Cloud's GitHub access
- Check you're using the correct branch name

---

## 📱 After Deployment

### Share Your App

Send this URL to anyone who needs to use the scraper:
```
https://[your-app-name].streamlit.app
```

No login required for users!

### Make Updates

To update your app:

1. Make changes to the code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update scraper"
   git push
   ```
3. Streamlit Cloud will **auto-deploy** the changes
4. Refresh your app URL to see updates

### Monitor Usage

In Streamlit Cloud dashboard:
- View app analytics
- See error logs
- Monitor resource usage
- Restart app if needed

---

## 🎉 You're Done!

Your Google Maps scraper is now:
- ✅ Live on the internet
- ✅ Accessible from anywhere
- ✅ Free to use
- ✅ Auto-updates when you push to GitHub

**Next Steps**:
1. Test your live app
2. Share with your team
3. Start scraping!

---

## 💡 Need Help?

If you get stuck:

1. **Check deployment logs** in Streamlit Cloud
2. **Verify all files** are committed and pushed
3. **Test locally first**: `streamlit run app.py`
4. **Contact support**: Streamlit Cloud has excellent support

---

**Happy Scraping!** 🚀
