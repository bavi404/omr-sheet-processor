# 🚀 Render Deployment - Quick Start (5 Minutes)

## Prerequisites ✅
- [x] GitHub repo: https://github.com/bavi404/omr-scanner-yolov8
- [x] Model uploaded to Google Drive
- [ ] Render account (create at render.com)

---

## 📤 Step 1: Upload Model to Google Drive

1. Upload `best.pt` to Google Drive
2. Right-click → Share → Get link
3. Make it "Anyone with the link can view"
4. Copy the FILE_ID from the URL:
   ```
   https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
   ```
5. Create direct download link:
   ```
   https://drive.google.com/uc?export=download&id=FILE_ID_HERE
   ```

**Save this link!** You'll need it in Step 3.

---

## 🌐 Step 2: Create Web Service on Render

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select **"omr-scanner-yolov8"** repository
5. Click **"Connect"**

---

## ⚙️ Step 3: Configure Service

### Basic Settings

| Setting | Value |
|---------|-------|
| **Name** | `omr-scanner-api` |
| **Region** | Oregon (US West) or closest to you |
| **Branch** | `main` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python download_model.py && gunicorn api_server:app` |

### Environment Variables

Click **"Add Environment Variable"** and add these:

| Key | Value |
|-----|-------|
| `MODEL_URL` | `https://drive.google.com/uc?export=download&id=YOUR_FILE_ID` |
| `MODEL_PATH` | `best.pt` |
| `PYTHON_VERSION` | `3.9.18` |

**Important:** Replace `YOUR_FILE_ID` with your actual Google Drive file ID!

### Plan

- Select **"Free"** plan
- Click **"Create Web Service"**

---

## ⏱️ Step 4: Wait for Deployment (3-5 minutes)

Watch the logs:
```
==> Downloading from GitHub...
==> Installing dependencies...
==> Downloading model...
==> Starting server...
==> Service is live!
```

---

## ✅ Step 5: Test Your API

Your API URL will be:
```
https://omr-scanner-api.onrender.com
```

### Test 1: Health Check
```bash
curl https://omr-scanner-api.onrender.com/api/health
```

Expected:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "service": "OMR Processing API"
}
```

### Test 2: Process OMR (with your image)
```bash
curl -X POST -F "file=@test_omr.jpg" \
  https://omr-scanner-api.onrender.com/api/process
```

---

## 🎉 Done! Share with Your Friend

Send them:
```
API URL: https://omr-scanner-api.onrender.com

Endpoints:
- POST /api/process - Upload OMR image
- GET /api/health - Check status

JavaScript example:
```javascript
async function processOMR(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(
        'https://omr-scanner-api.onrender.com/api/process',
        { method: 'POST', body: formData }
    );
    
    return await response.json();
}
```

---

## 🐛 Troubleshooting

### "Model not loaded"
- Check MODEL_URL in environment variables
- Verify Google Drive link is direct download link
- Check logs for download errors

### "Build failed"
- Check Python version (should be 3.9.18)
- Verify requirements.txt is correct
- Check build logs for specific error

### "Service unavailable" 
- Free tier sleeps after 15 min inactivity
- First request after sleep takes 30-60s
- Or upgrade to paid plan ($7/month, no sleep)

### Check Logs
Dashboard → Your Service → Logs

---

## 🔄 Update Your Deployment

Push to GitHub = auto-deploy! ✨

```bash
git add .
git commit -m "Update API"
git push
```

Render automatically deploys new changes.

---

## 📊 Free Tier Limits

- ✅ 512 MB RAM
- ✅ 750 hours/month
- ❌ Sleeps after 15 min inactivity
- ❌ Slower builds

**Upgrade to $7/month for:**
- 2 GB RAM
- No sleep
- Faster builds

---

## 📝 Full Documentation

See **RENDER_DEPLOYMENT.md** for complete guide with:
- Security setup
- Custom domains
- Monitoring
- Scaling options
- Advanced configuration

---

**Estimated time: 5-10 minutes**

**Cost: FREE** (upgrade optional)

**Your API will be live at:**
```
https://your-app-name.onrender.com
```

🎊 **READY FOR PRODUCTION!** 🎊

