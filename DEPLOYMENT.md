# Deployment Guide: Vercel (Frontend) + Render (Backend)

## Step 1: Push to GitHub

```bash
cd /Users/thinhnguyen/Downloads/runitbackhanoi
git init
git add -A
git commit -m "Initial commit"
gh repo create runitbackhanoi --public --push --source .
```

## Step 2: Deploy Backend on Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **New > Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Name:** `runitbackhanoi-api`
   - **Root Directory:** `backend`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. Add **Environment Variables:**
   - `OPENAI_API_KEY` — your API key
   - `OPENAI_MODEL` — `gpt-4o-mini`
   - `GOOGLE_SHEETS_ID` — your sheet ID (optional, demo mode works without it)
   - `GOOGLE_CREDENTIALS_JSON` — paste your entire `credentials.json` content as a string (optional)
6. Click **Deploy**

Your backend URL will be something like: `https://runitbackhanoi-api.onrender.com`

## Step 3: Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) and sign up (free)
2. Click **Import Project** and select your GitHub repo
3. Configure:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite (auto-detected)
4. Add **Environment Variable:**
   - `VITE_API_URL` = `https://runitbackhanoi-api.onrender.com/api` (use your actual Render URL from step 2)
5. Click **Deploy**

## Step 4: Update vercel.json with your actual Render URL

The file `frontend/vercel.json` contains a placeholder URL. Update the rewrite destination to match your actual Render URL:

```json
"destination": "https://YOUR-ACTUAL-RENDER-URL.onrender.com/api/:path*"
```

## Notes

- Render free tier **sleeps after 15 min of inactivity** — first request after sleep takes ~30s to cold-start.
- The frontend uses either the Vercel rewrite (`/api/*` → Render) or the `VITE_API_URL` env var — both approaches work, but you only need one.
- Demo mode works without Google Sheets or OpenAI keys configured.
