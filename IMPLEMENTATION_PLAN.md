# RunItBackHanoi - Implementation Plan

## Overview

Build an AI-powered basketball matchmaking chatbot for Hanoi players. The system uses a RAG-lite approach where structured data from Google Sheets is passed into OpenAI's system prompt for intelligent match recommendations.

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  React Frontend │────▶│  Python Backend │────▶│  Google Sheets  │
│  (Material UI)  │     │    (FastAPI)    │     │   (Database)    │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │                 │
                        │   OpenAI API    │
                        │  (GPT-4o-mini)  │
                        │                 │
                        └─────────────────┘
```

---

## Project Structure

```
runitbackhanoi/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── sheets_service.py    # Google Sheets integration
│   ├── openai_service.py    # OpenAI API integration
│   ├── models.py            # Pydantic models
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx          # Main app component
│   │   ├── components/
│   │   │   ├── Chat.jsx     # Chat interface
│   │   │   ├── Message.jsx  # Message bubble component
│   │   │   └── Header.jsx   # App header
│   │   ├── services/
│   │   │   └── api.js       # API service
│   │   ├── theme.js         # Material UI theme
│   │   └── index.jsx        # Entry point
│   └── package.json
│
├── IMPLEMENTATION_PLAN.md
└── README.md
```

---

## Phase 1: Backend Implementation (Python + FastAPI)

### 1.1 Dependencies (requirements.txt)
```
fastapi==0.109.0
uvicorn==0.27.0
python-dotenv==1.0.0
openai==1.12.0
google-api-python-client==2.116.0
google-auth-oauthlib==1.2.0
pydantic==2.5.3
httpx==0.26.0
```

### 1.2 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Send message to AI chatbot |
| `/api/players` | POST | Register new player |
| `/api/players/{phone}` | GET | Get player by phone |
| `/api/matches` | GET | Get all open matches |
| `/api/courts` | GET | Get all courts |
| `/api/health` | GET | Health check |

### 1.3 Google Sheets Structure

**Sheet 1: Courts (san_bong)**
| Column | Description |
|--------|-------------|
| id | Unique court ID |
| name | Court name |
| address | Full address |
| district | District name |
| price | Price per hour (VND) |
| opening_hours | Operating hours |
| phone | Contact phone |

**Sheet 2: Players (nguoi_choi)**
| Column | Description |
|--------|-------------|
| id | Unique player ID |
| name | Player name |
| phone | Phone number |
| skill_level | Beginner/Intermediate/Advanced |
| preferred_district | Preferred area |
| created_at | Registration date |

**Sheet 3: Matches (tran_dau)**
| Column | Description |
|--------|-------------|
| id | Match ID |
| court_id | Court reference |
| datetime | Match date/time |
| skill_level | Required skill level |
| max_players | Maximum players (default: 10) |
| current_players | Current player count |
| player_ids | Comma-separated player IDs |
| status | open/full/completed/cancelled |
| created_by | Creator player ID |

### 1.4 System Prompt Template

```python
SYSTEM_PROMPT = """
Bạn là trợ lý AI của RunItBackHanoi - nền tảng ghép trận bóng rổ tại Hà Nội.

## Vai trò của bạn:
- Giúp người chơi tìm trận đấu phù hợp
- Hỗ trợ đăng ký tham gia trận
- Tạo trận đấu mới
- Cung cấp thông tin sân bóng rổ

## Dữ liệu sân bóng rổ hiện có:
{courts_data}

## Các trận đấu đang mở:
{matches_data}

## Quy tắc ghép trận:
1. Ưu tiên ghép theo trình độ tương đương
2. Ưu tiên sân gần khu vực người chơi
3. Kiểm tra thời gian phù hợp
4. Nếu không có trận phù hợp, gợi ý tạo trận mới

## Trình độ:
- Beginner: Mới chơi, đang học cơ bản
- Intermediate: Chơi được, hiểu chiến thuật cơ bản
- Advanced: Chơi tốt, thi đấu thường xuyên

## Cách trả lời:
- Dùng tiếng Việt, thân thiện, ngắn gọn
- Luôn đưa ra gợi ý cụ thể dựa trên dữ liệu
- Hỏi thêm nếu thiếu thông tin (trình độ, khu vực, thời gian)
"""
```

---

## Phase 2: Frontend Implementation (React + Material UI)

### 2.1 Dependencies (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@mui/material": "^5.15.0",
    "@mui/icons-material": "^5.15.0",
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0",
    "axios": "^1.6.0"
  }
}
```

### 2.2 UI Components

1. **Header**: App title, logo
2. **Chat Container**: Scrollable message list
3. **Message Bubble**: User/AI message display
4. **Input Area**: Text input + send button
5. **Registration Modal**: New player registration form

### 2.3 User Flow

```
1. User opens website
   └── If not registered → Show registration modal
       └── Collect: Name, Phone, Skill Level, Preferred District
       └── Save to Google Sheets

2. User sends message
   └── Frontend calls /api/chat
   └── Backend fetches latest data from Sheets
   └── Backend builds system prompt with data
   └── Backend calls OpenAI API
   └── AI response returned to frontend

3. User joins match
   └── AI confirms join request
   └── Backend updates Sheets (add player to match)
   └── AI confirms success
```

---

## Phase 3: Basketball Court Data for Demo

Based on research, here are basketball courts in Hanoi for the demo:

| ID | Name | Address | District | Price (VND/hr) | Hours |
|----|------|---------|----------|----------------|-------|
| 1 | Van Phuc Sports Center | 73 Van Bao | Ba Dinh | 150,000 | 6:00-22:00 |
| 2 | Architecture University Court | Nguyen Trai | Thanh Xuan | Free | 6:00-21:00 |
| 3 | Medical University Court | Ton That Tung | Dong Da | Free | 6:00-21:00 |
| 4 | New Quarter Basketball | Alley 612 Hoang Hoa Tham | Ba Dinh | 200,000 | 6:00-22:00 |
| 5 | My Dinh Basketball Court | Nhan My Ward | Nam Tu Liem | 100,000 | 6:00-22:00 |
| 6 | Nguyen Thi Thap Court | Nguyen Thi Thap | Cau Giay | 120,000 | 6:00-22:00 |
| 7 | SkyTrap Basketball | 1 Trinh Van Bo | Nam Tu Liem | 180,000 | 7:00-22:00 |
| 8 | Level Basketball Court | The Nine Building | Cau Giay | 200,000 | 8:00-22:00 |
| 9 | Bach Khoa Stadium | Le Thanh Nghi | Hai Ba Trung | 80,000 | 6:00-21:00 |
| 10 | Chu Van An School | Thuy Khue | Tay Ho | Free | 17:00-20:00 |
| 11 | Hanoi-Amsterdam School | Nam Cao | Cau Giay | Free | 17:00-20:00 |
| 12 | Su Pham Court | 80 Tran Quoc Hoan | Cau Giay | Free | 6:00-21:00 |

---

## Phase 4: Environment Setup

### 4.1 Required API Keys

1. **OpenAI API Key**
   - Get from: https://platform.openai.com/api-keys
   - Model: gpt-4o-mini

2. **Google Sheets API**
   - Create project at: https://console.cloud.google.com
   - Enable Google Sheets API
   - Create Service Account
   - Download credentials JSON
   - Share Google Sheet with service account email

### 4.2 Environment Variables (.env)

```env
# OpenAI
OPENAI_API_KEY=sk-xxx

# Google Sheets
GOOGLE_SHEETS_ID=your-sheet-id
GOOGLE_CREDENTIALS_PATH=./credentials.json

# Server
PORT=8000
FRONTEND_URL=http://localhost:3000
```

---

## Phase 5: Implementation Steps

### Step 1: Set up Google Sheet
- Create new Google Sheet with 3 tabs: Courts, Players, Matches
- Populate Courts tab with demo data
- Share with service account

### Step 2: Backend Development
- Initialize FastAPI project
- Implement Google Sheets service
- Implement OpenAI service
- Create API endpoints
- Add CORS middleware

### Step 3: Frontend Development
- Create React app with Vite
- Install Material UI
- Build chat interface
- Build registration modal
- Connect to backend API

### Step 4: Integration Testing
- Test chat functionality
- Test player registration
- Test match joining
- Test match creation

### Step 5: Deployment (Optional)
- Backend: Railway, Render, or Heroku
- Frontend: Vercel, Netlify, or GitHub Pages

---

## Sample API Interactions

### Chat Request
```json
POST /api/chat
{
  "message": "Tôi muốn chơi bóng tối nay ở Cầu Giấy",
  "player_id": "P001"
}
```

### Chat Response
```json
{
  "response": "Có 2 trận đấu phù hợp với bạn tối nay ở khu vực Cầu Giấy:\n\n1. Trận #5: Sân Nguyễn Thị Thập, 19h00, trình Trung bình, còn 3 chỗ\n2. Trận #8: Sân Level, 20h00, trình Nâng cao, còn 2 chỗ\n\nBạn muốn tham gia trận nào?",
  "actions": [
    {"type": "join_match", "match_id": "M005"},
    {"type": "join_match", "match_id": "M008"}
  ]
}
```

### Player Registration
```json
POST /api/players
{
  "name": "Nguyen Van A",
  "phone": "0912345678",
  "skill_level": "Intermediate",
  "preferred_district": "Cau Giay"
}
```

---

## Security Considerations

1. **API Keys**: Never expose in frontend code
2. **Rate Limiting**: Implement on chat endpoint
3. **Input Validation**: Sanitize all user inputs
4. **CORS**: Restrict to known origins in production

---

## Estimated Effort

| Phase | Tasks |
|-------|-------|
| Phase 1 | Backend setup, Sheets integration, OpenAI integration |
| Phase 2 | Frontend UI, Chat interface, Registration flow |
| Phase 3 | Data population, Testing |
| Phase 4 | Integration, Bug fixes |
| Phase 5 | Deployment (optional) |

---

## Next Steps

1. Create the Google Sheet and populate with court data
2. Set up the Python backend with FastAPI
3. Build the React frontend with Material UI
4. Test the complete flow
5. Deploy for demo

