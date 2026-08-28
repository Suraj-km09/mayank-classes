# 🚀 Mayank Classes - Production & Railway Deployment Guide

This repository is configured for 1-click deployment on [Railway](https://railway.com/) and standard production hosting platforms (Render, Fly.io, DigitalOcean, VPS).

---

## 📦 What Has Been Configured for Production
- **`Procfile`**: Defines the Gunicorn WSGI process runner (`gunicorn config.wsgi:application`).
- **`railway.json` & `nixpacks.toml`**: Automated build steps, static files collection (`collectstatic`), and database migrations (`migrate`).
- **`requirements.txt`**: Pinned production dependencies including `gunicorn`, `whitenoise`, `dj-database-url`, `psycopg2-binary`, `pillow`, `requests`, and `python-dotenv`.
- **`config/settings.py`**:
  - Dynamic `DATABASE_URL` parsing (auto-connects to Railway PostgreSQL if provisioned, or falls back to SQLite).
  - Production `WhiteNoise` static files serving with compression.
  - Automatic `CSRF_TRUSTED_ORIGINS` and `ALLOWED_HOSTS` configuration.
  - Reverse proxy HTTPS header support (`SECURE_PROXY_SSL_HEADER`).
- **`.gitignore`**: Protects `.env`, virtual environments, bytecode, and sensitive local secrets from being committed to GitHub.

---

## 🛠️ Step 1: Push Code to Your GitHub Repository

Run the following commands in your terminal:

```bash
# 1. Initialize git repository (if not already done)
git init

# 2. Add all files
git add .

# 3. Commit the changes
git commit -m "feat: complete production-ready Mayank Classes platform for Railway"

# 4. Rename main branch
git branch -M main

# 5. Link to your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 6. Push to GitHub
git push -u origin main
```

---

## 🚂 Step 2: Deploy on Railway in 3 Easy Steps

1. **Log in to [Railway.com](https://railway.com/)** and click **"New Project"**.
2. Select **"Deploy from GitHub repo"** and choose your `mayank-classes` repository.
3. Click **"Deploy Now"**.

---

## ⚙️ Step 3: Configure Environment Variables in Railway

Go to your Railway service dashboard ➔ **"Variables"** tab ➔ Click **"Add Variable"** or **"RAW Editor"** and paste:

```env
SECRET_KEY=your-production-super-secret-key-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://*.up.railway.app

# Google Gemini AI Chatbot API Key (From Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# Gmail SMTP Email Delivery
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_google_app_password
DEFAULT_FROM_EMAIL=Mayank Classes <admissions@mayankclasses.com>
ADMIN_EMAIL_NOTIFICATION=your_admin_email@gmail.com
```

> 💡 **PostgreSQL Database (Optional but Recommended)**:
> In Railway, click **"+ New"** ➔ **"Database"** ➔ **"Add PostgreSQL"**.
> Railway will automatically inject the `DATABASE_URL` environment variable into your Django service, and Django will seamlessly connect to PostgreSQL with zero manual configuration!

---

## 🌐 Step 4: Generate Domain

1. In your Railway service dashboard, go to the **"Settings"** tab.
2. Under **"Networking"**, click **"Generate Domain"** (e.g. `mayank-classes-production.up.railway.app`).
3. Your website is now **LIVE** worldwide with SSL HTTPS! 🎉

---

## 👤 Step 5: Create Superuser / Admin Account on Railway

Once deployed, open Railway's service terminal or run using Railway CLI:

```bash
railway run python manage.py createsuperuser
```

Or run seed demo data:
```bash
railway run python manage.py seed_data
```
