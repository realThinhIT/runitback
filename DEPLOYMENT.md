# Deployment Guide: Vercel (Frontend) + Railway (Backend)

## Step 1: Push to GitHub

```bash
git init
git add -A
git commit -m "Initial commit"
gh repo create runitbackhanoi --public --push --source .
```

## Step 2: Deploy Backend on Railway

1. Go to [railway.com](https://railway.com) and sign up (free — $5 credit/month, no cold starts)
2. Click **New Project > Deploy from GitHub Repo**
3. Select your GitHub repo
4. Configure:
   - **Root Directory:** `backend`
   - Railway auto-detects Python and uses `requirements.txt`
5. Add **Environment Variables** (Settings > Variables):
   - `OPENAI_API_KEY` — your API key
   - `OPENAI_MODEL` — `gpt-4o-mini`
   - `GOOGLE_SHEETS_ID` — your sheet ID (optional, demo mode works without it)
   - `GOOGLE_CREDENTIALS_JSON` — paste your entire `credentials.json` content as a string (optional)
   - `PORT` — `8000`
6. Go to **Settings > Networking** and click **Generate Domain** to get a public URL

Your backend URL will be something like: `https://runitbackhanoi-api-production.up.railway.app`

## Step 3: Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) and sign up (free)
2. Click **Import Project** and select your GitHub repo
3. Configure:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite (auto-detected)
4. Add **Environment Variable:**
   - `VITE_API_URL` = `https://YOUR-RAILWAY-URL.up.railway.app/api` (use your actual Railway URL from step 2)
5. Click **Deploy**

## Step 4: Update vercel.json with your actual Railway URL

The file `frontend/vercel.json` contains a placeholder URL. Update the rewrite destination to match your actual Railway URL:

```json
"destination": "https://YOUR-RAILWAY-URL.up.railway.app/api/:path*"
```

## Notes

- Railway has **no cold starts** — your backend stays warm within the free $5/month credit.
- The frontend uses either the Vercel rewrite (`/api/*` → Railway) or the `VITE_API_URL` env var — both approaches work, but you only need one.
- Demo mode works without Google Sheets or OpenAI keys configured.
- A `backend/railway.toml` is included to configure the start command automatically.
