# 🚀 Deploy to Render.com - Step-by-Step Guide

Complete guide to deploy your OMR Scanner API to Render.com (Free tier available!)

## ✅ Prerequisites

- [x] Code pushed to GitHub ✓ (https://github.com/bavi404/omr-scanner-yolov8)
- [x] Render.com account (free) - Sign up at https://render.com

---

## 📋 Step-by-Step Deployment

### Step 1: Create Render Account

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub (recommended) or email
4. Verify your email

---

### Step 2: Connect GitHub Repository

1. On Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Click **"Connect account"** if GitHub not connected
4. Authorize Render to access your GitHub repos
5. Find and select **"omr-scanner-yolov8"** from the list
6. Click **"Connect"**

---

### Step 3: Configure Web Service

Fill in these settings:

#### **Basic Settings**

| Field | Value |
|-------|-------|
| **Name** | `omr-scanner-api` (or your choice) |
| **Region** | Choose closest to you (e.g., Oregon, Frankfurt) |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Runtime** | `Python 3` (auto-detected) |

#### **Build & Deploy Settings**

| Field | Value |
|-------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn api_server:app` |

#### **Plan**

- Select **"Free"** (starts with $0/month)
- Free tier limitations:
  - 512 MB RAM
  - Sleeps after 15 min inactivity
  - 750 hours/month free

---

### Step 4: Add Environment Variables

Scroll down to **"Environment Variables"** section:

Click **"Add Environment Variable"** and add:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.9.18` | Specify Python version |
| `MODEL_PATH` | `best.pt` | Local path after download |
| `PORT` | `5000` | Default Flask port |

---

### Step 5: Handle Model Weights

**⚠️ IMPORTANT**: Your model file (`best.pt`) is not in GitHub (too large).

#### **Option A: Download on Startup (Recommended)**

Add a startup script to download the model:

1. Create `download_model.py` in your repo:

```python
import os
import requests

MODEL_URL = os.getenv('MODEL_URL', 'YOUR_GOOGLE_DRIVE_DIRECT_LINK')
MODEL_PATH = 'best.pt'

if not os.path.exists(MODEL_PATH):
    print("Downloading model weights...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, 'wb') as f:
        f.write(response.content)
    print("Model downloaded successfully!")
else:
    print("Model already exists.")
```

2. Update your **Start Command**:
```bash
python download_model.py && gunicorn api_server:app
```

3. Add environment variable:
   - Key: `MODEL_URL`
   - Value: Your Google Drive direct download link

**How to get Google Drive direct link:**
```
Original: https://drive.google.com/file/d/FILE_ID/view?usp=sharing
Direct:   https://drive.google.com/uc?export=download&id=FILE_ID
```

#### **Option B: Use External Storage**

Host model on:
- AWS S3
- Hugging Face Hub
- Cloudinary
- Any CDN with direct download link

---

### Step 6: Deploy!

1. Scroll to bottom and click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies
   - Download model (if configured)
   - Start the server
3. Watch the **"Logs"** tab for deployment progress

**Deployment takes 3-5 minutes.**

---

### Step 7: Get Your API URL

Once deployed, you'll see:

```
🎉 Live at https://your-app-name.onrender.com
```

**Your API endpoints:**
- `https://your-app-name.onrender.com/api/health`
- `https://your-app-name.onrender.com/api/process`
- `https://your-app-name.onrender.com/api/model-info`

---

## ✅ Verify Deployment

### Test 1: Health Check

```bash
curl https://your-app-name.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "service": "OMR Processing API",
  "version": "1.0.0"
}
```

### Test 2: Process OMR

```bash
curl -X POST -F "file=@test_omr.jpg" \
  https://your-app-name.onrender.com/api/process
```

---

## ⚙️ Configuration Files Needed

Make sure these files exist in your repo (they already do!):

### 1. `requirements.txt` ✓
```
opencv-python>=4.8.0
ultralytics>=8.0.0
easyocr>=1.7.0
flask>=2.3.0
flask-cors>=4.0.0
numpy>=1.24.0
torch>=2.0.0
Pillow>=10.0.0
gunicorn>=21.2.0
```

### 2. `Procfile` ✓
```
web: gunicorn api_server:app
```

### 3. `api_server.py` ✓
Already configured with proper port handling.

---

## 🔧 Advanced Configuration

### Custom Domain

1. Go to your service settings
2. Click **"Custom Domain"**
3. Add your domain (e.g., `api.yourdomain.com`)
4. Configure DNS as instructed

### Auto-Deploy

Render automatically deploys when you push to GitHub:

```bash
# Make changes locally
git add .
git commit -m "Update API"
git push

# Render auto-deploys! ✨
```

### Persistent Disk (Paid)

To keep model weights across deployments:

1. Settings → **"Disks"**
2. Add disk: `/opt/render/project/models`
3. Store model there instead of project root

---

## 🐛 Troubleshooting

### Issue: "Build Failed"

**Check Build Logs:**
- Missing dependencies? Update `requirements.txt`
- Python version issue? Set `PYTHON_VERSION` env var

### Issue: "Model Not Loading"

**Possible causes:**
1. Model URL is wrong
2. Model download failed (check logs)
3. Not enough RAM (512MB on free tier)

**Solution:**
- Verify MODEL_URL in environment variables
- Check logs for download errors
- Consider upgrading to paid plan ($7/month, 2GB RAM)

### Issue: "503 Service Unavailable"

**Cause:** Free tier sleeps after 15 min inactivity

**Solution:**
- First request after sleep takes 30-60 seconds
- Use a ping service (e.g., UptimeRobot)
- Or upgrade to paid plan (no sleep)

### Issue: "Application Error"

**Check Logs:**
1. Go to service dashboard
2. Click **"Logs"** tab
3. Look for error messages

**Common fixes:**
- Wrong start command
- Missing environment variables
- Port binding issues (use Render's $PORT)

---

## 💰 Pricing

### Free Tier
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ 750 hours/month
- ❌ Sleeps after 15 min inactivity
- ❌ Build time: slower

**Cost:** $0/month

### Starter Plan ($7/month)
- ✅ 2 GB RAM
- ✅ Shared CPU
- ✅ Always on (no sleep)
- ✅ Faster builds

### Standard Plan ($25/month)
- ✅ 4 GB RAM
- ✅ Dedicated CPU
- ✅ Better performance

---

## 🔒 Security Best Practices

### 1. Add API Key Authentication

Add to environment variables:
```
API_KEY=your-secret-key-here
```

Update `api_server.py` to check this key.

### 2. CORS Configuration

Update allowed origins in `api_server.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourwebsite.com"],  # Your friend's website
        "methods": ["GET", "POST", "OPTIONS"]
    }
})
```

### 3. Rate Limiting

Consider adding rate limiting to prevent abuse.

---

## 📊 Monitoring

### View Logs

Real-time:
```
Dashboard → Your Service → Logs
```

### Metrics

Dashboard shows:
- CPU usage
- Memory usage
- Request count
- Response times

### Alerts

Set up email alerts for:
- Service down
- High error rate
- Memory issues

---

## 🔄 Update Your Deployment

### Method 1: Git Push (Auto-Deploy)

```bash
# Make changes
git add .
git commit -m "Fix bubble detection"
git push

# Render auto-deploys ✨
```

### Method 2: Manual Deploy

1. Dashboard → Your Service
2. Click **"Manual Deploy"**
3. Select branch
4. Click **"Deploy"**

---

## 📝 Complete Setup Checklist

- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Configure web service settings
- [ ] Add environment variables
- [ ] Upload model to Google Drive
- [ ] Get direct download link
- [ ] Add MODEL_URL to env vars
- [ ] Deploy service
- [ ] Test `/api/health` endpoint
- [ ] Test `/api/process` endpoint
- [ ] Update your friend with API URL
- [ ] Configure CORS for their website

---

## 🌐 Integration with Website

After deployment, share this with your friend:

```javascript
// Replace with your actual Render URL
const API_URL = 'https://your-app-name.onrender.com';

async function processOMR(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_URL}/api/process`, {
        method: 'POST',
        body: formData
    });
    
    return await response.json();
}
```

---

## 🎯 Your Deployed API

Once complete, you'll have:

✅ **Live API URL:** `https://your-app-name.onrender.com`
✅ **Auto-deploy:** Push to GitHub = auto update
✅ **SSL/HTTPS:** Automatic, free
✅ **Global CDN:** Fast worldwide
✅ **Monitoring:** Built-in logs and metrics
✅ **Scalable:** Easy to upgrade

---

## 📞 Support

**Render Support:**
- Documentation: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

**Your Repository:**
- Issues: https://github.com/bavi404/omr-scanner-yolov8/issues

---

## ⏱️ Estimated Time

- Account setup: 2 minutes
- Repository connection: 1 minute
- Configuration: 3 minutes
- Model upload to Drive: 5 minutes
- Deployment: 3-5 minutes

**Total: ~15 minutes** ⚡

---

## 🎉 Success!

Once deployed, your OMR scanner will be:
- 🌐 Accessible worldwide
- 🔒 HTTPS encrypted
- 🚀 Ready for production
- 💰 Free to start

**Your API will be live at:**
```
https://your-app-name.onrender.com
```

Share this URL with your friend to integrate with their website! 🎊

