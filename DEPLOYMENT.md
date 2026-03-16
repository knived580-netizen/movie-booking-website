# 🚀 Django Movie Booking - Deployment Guide

## ✅ What Has Been Prepared

Your project is now ready for production deployment with:
- ✅ `requirements.txt` - All project dependencies
- ✅ `Procfile` - Heroku/Render configuration
- ✅ `.env.example` - Environment variables template
- ✅ `runtime.txt` - Python version specification
- ✅ `.gitignore` - Git ignore rules
- ✅ `settings.py` - Updated with production security settings

---

## 🎯 Deployment Options

### Option 1: **Render** (Recommended - Free Tier Available)
Easiest for beginners, free tier includes web service.

#### Steps:
1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/moviebooking.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://render.com
   - Sign up with GitHub
   - Click **New +** → **Web Service**
   - Connect your GitHub repo
   - Fill in details:
     - **Name**: moviebooking
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - **Start Command**: `gunicorn moviebooking.wsgi`
   
3. **Set Environment Variables** (in Render Dashboard)
   - `DEBUG` = `False`
   - `SECRET_KEY` = Generate new: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
   - `ALLOWED_HOSTS` = `your-app.onrender.com`

---

### Option 2: **PythonAnywhere** (Beginner-Friendly)
Paid but very easy to set up.

#### Steps:
1. Go to https://www.pythonanywhere.com
2. Create account
3. Upload your code via Git or ZIP
4. Set up a Web app with Python 3.13
5. Configure settings in **Web** tab
6. Set environment variables in `.env` file

---

### Option 3: **DigitalOcean App Platform**
Similar to Render, good documentation.

---

## 📋 Pre-Deployment Checklist

Before deploying, run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test production server
python manage.py runserver --settings=moviebooking.settings
```

---

## 🔐 Production Security

Your `settings.py` now includes automatic security settings when `DEBUG=False`:

✅ HTTPS redirection  
✅ Secure cookies  
✅ HSTS headers  
✅ CSRF protection  

---

## 🗄️ Database Upgrade (Optional but Recommended)

For production, upgrade from SQLite to PostgreSQL:

1. **Install PostgreSQL add-on** (most hosting platforms)
2. **Update settings.py** to use PostgreSQL
3. **Update requirements.txt** to include `psycopg2`

---

## 📚 Next Steps

1. ✅ Create a `.env` file locally (copy from `.env.example`)
2. ✅ Test locally: `python manage.py runserver`
3. ✅ Push to GitHub
4. ✅ Choose a hosting platform and deploy
5. ✅ Monitor logs for errors

Need help with a specific platform? Let me know!
