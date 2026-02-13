# RunItBackHanoi

AI-powered basketball matchmaking chatbot for Hanoi. Uses GPT-4o-mini with RAG-lite approach to help players find and join basketball games.

## Features

- AI chatbot that understands natural language (Vietnamese with diacritics)
- Find basketball matches by skill level, location, and time
- Join existing matches or create new ones
- View basketball court information in Hanoi
- Player registration and persistence via Google Sheets
- Supports multiple AI providers (OpenAI, OpenRouter, etc.)

## Architecture

```
React Frontend (Material UI) → Python Backend (FastAPI) → Google Sheets + OpenAI-compatible API
```

## Quick Start (Demo Mode)

The app works in demo mode without any API configuration. Demo mode uses:
- Pre-loaded basketball court data (12 courts in Hanoi)
- Sample matches
- Basic AI responses in Vietnamese

### 1. Start Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs at: http://localhost:8000

### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## Production Setup

### 1. AI Provider Configuration

The app supports multiple OpenAI-compatible APIs:

#### Option A: OpenAI (Direct)
```env
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

#### Option B: OpenRouter
```env
OPENAI_API_KEY=sk-or-your-openrouter-key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4o-mini
```

#### Option C: Other Providers (Together, Groq, etc.)
```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.together.xyz/v1
OPENAI_MODEL=meta-llama/Llama-3-70b-chat-hf
```

### 2. Google Sheets Setup

#### Step 1: Create Google Cloud Project
1. Go to https://console.cloud.google.com
2. Create a new project
3. Enable "Google Sheets API"

#### Step 2: Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Create a new service account
3. Download the JSON credentials file
4. Save as `backend/credentials.json`

#### Step 3: Create Google Sheet
1. Create a new Google Sheet
2. Name it "RunItBackHanoi"
3. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[SHEET_ID_HERE]/edit
   ```
4. Share the sheet with your service account email (found in credentials.json)

#### Step 4: Seed Demo Data

Once your `.env` is configured (see step 3 below), run the seed script to create the sheet tabs and populate them with demo data:

```bash
cd backend
python seed_demo_data.py
```

This will create three tabs and fill them with sample data:

- **Courts** — 12 basketball courts across Hanoi (free and paid)
- **Players** — 12 demo players with varied skill levels and districts
- **Matches** — 5 upcoming matches with pre-assigned players

You can re-run the script at any time to reset the sheet to a clean demo state.

### 3. Environment Configuration

Create `backend/.env`:

```env
# OpenAI API (or OpenRouter/other compatible APIs)
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
# OPENAI_BASE_URL=https://openrouter.ai/api/v1  # Uncomment for OpenRouter

# Google Sheets
GOOGLE_SHEETS_ID=your-sheet-id-here
GOOGLE_CREDENTIALS_PATH=./credentials.json

# Server
PORT=8000
FRONTEND_URL=http://localhost:5173
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Send message to AI chatbot |
| `/api/players` | POST | Register new player |
| `/api/players/{phone}` | GET | Get player by phone |
| `/api/courts` | GET | Get all courts |
| `/api/matches` | GET | Get all matches |
| `/api/matches/open` | GET | Get open matches |
| `/api/matches/{id}/join` | POST | Join a match |

## Sample Conversation

**User:** "Tôi muốn chơi bóng tối nay ở Cầu Giấy"

**AI:** "Hiện có 2 trận đấu phù hợp với bạn tối nay ở khu vực Cầu Giấy:
- Trận #M001: Sân Nguyễn Thị Thập, 19h00, trình Intermediate, còn 6 chỗ
- Trận #M002: Sân Level Basketball, 20h00, trình Advanced, còn 4 chỗ

Bạn muốn tham gia trận nào?"

**User:** "Đăng ký trận 1 cho tôi"

**AI:** "Đã ghi nhận! Bạn đã tham gia trận #M001 tại sân Nguyễn Thị Thập, 19h00. Hẹn gặp bạn!"

## Tech Stack

- **Frontend:** React 18, Material UI 5, Vite
- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **AI:** OpenAI GPT-4o-mini (or any OpenAI-compatible API)
- **Database:** Google Sheets API

## Project Structure

```
runitbackhanoi/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── sheets_service.py    # Google Sheets integration
│   ├── openai_service.py    # OpenAI/OpenRouter integration
│   ├── models.py            # Pydantic models
│   ├── seed_demo_data.py    # Seed Google Sheets with demo data
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── Chat.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── Message.jsx
│   │   │   └── RegisterModal.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── theme.js
│   └── package.json
│
├── IMPLEMENTATION_PLAN.md
└── README.md
```

## License

MIT
