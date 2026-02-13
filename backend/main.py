import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List

# Load environment variables from .env file in the backend directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Debug: Print loaded config (remove in production)
print(f"Loading .env from: {env_path}")
print(f"OPENAI_API_KEY set: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL', 'Not set (using OpenAI default)')}")
print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}")

from models import (
    ChatRequest, ChatResponse, Player, PlayerCreateRequest,
    Court, Match, MatchStatus, SkillLevel
)
from sheets_service import get_sheets_service
from openai_service import get_openai_service

# Initialize FastAPI app
app = FastAPI(
    title="RunItBackHanoi API",
    description="AI-powered basketball matchmaking chatbot for Hanoi",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
sheets_service = get_sheets_service()
openai_service = get_openai_service()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to RunItBackHanoi API",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "RunItBackHanoi"}


# ===== CHAT ENDPOINTS =====

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the AI chatbot.
    The AI will use current data from Google Sheets to provide relevant responses.
    """
    # Get current data
    courts = sheets_service.get_all_courts()
    matches = sheets_service.get_open_matches()

    # Get player info if provided
    player = None
    if request.player_id:
        player = sheets_service.get_player_by_id(request.player_id)

    # Get AI response
    response = openai_service.chat(
        message=request.message,
        courts=courts,
        matches=matches,
        player=player,
        conversation_history=request.conversation_history
    )

    # Parse ACTION block from AI response
    action_result = None
    clean_response = response
    import re, json
    action_match = re.search(r'\[ACTION:(.*?)\]', response, re.DOTALL)
    if action_match:
        clean_response = response[:action_match.start()].rstrip()
        try:
            action = json.loads(action_match.group(1))
            action_type = action.get("type")
            player_id = request.player_id

            if action_type == "join_match" and player_id:
                match_id = action["match_id"]
                success = sheets_service.join_match(match_id, player_id)
                action_result = {"type": "join_match", "match_id": match_id, "success": success}

            elif action_type == "create_match":
                new_match = Match(
                    court_id=action["court_id"],
                    datetime=action["datetime"],
                    skill_level=SkillLevel(action["skill_level"]),
                    max_players=int(action.get("max_players", 10)),
                    current_players=1 if player_id else 0,
                    player_ids=[player_id] if player_id else [],
                    created_by=player_id,
                )
                created = sheets_service.create_match(new_match)
                if created:
                    action_result = {"type": "create_match", "match_id": created.id, "success": True}
                    # Replace placeholder in response text
                    clean_response = clean_response.replace("#[NEW]", f"#{created.id}")
                else:
                    action_result = {"type": "create_match", "success": False}

            elif action_type == "leave_match" and player_id:
                match_id = action["match_id"]
                success = sheets_service.leave_match(match_id, player_id)
                action_result = {"type": "leave_match", "match_id": match_id, "success": success}

            elif action_type == "update_player" and player_id:
                fields = {k: v for k, v in action.items() if k != "type"}
                success = sheets_service.update_player(player_id, **fields)
                action_result = {"type": "update_player", "success": success}

        except Exception as e:
            print(f"Error processing action: {e}")
            action_result = {"type": action.get("type", "unknown"), "success": False, "error": str(e)}

    return ChatResponse(response=clean_response, player_id=request.player_id, action_result=action_result)


# ===== PLAYER ENDPOINTS =====

@app.post("/api/players", response_model=Player)
async def create_player(request: PlayerCreateRequest):
    """Register a new player."""
    player = Player(
        name=request.name,
        phone=request.phone,
        skill_level=request.skill_level,
        preferred_district=request.preferred_district
    )

    created = sheets_service.create_player(player)
    if created:
        return created
    raise HTTPException(status_code=500, detail="Failed to create player")


@app.get("/api/players/{phone}", response_model=Player)
async def get_player_by_phone(phone: str):
    """Get a player by phone number."""
    player = sheets_service.get_player_by_phone(phone)
    if player:
        return player
    raise HTTPException(status_code=404, detail="Player not found")


@app.get("/api/players/id/{player_id}", response_model=Player)
async def get_player_by_id(player_id: str):
    """Get a player by ID."""
    player = sheets_service.get_player_by_id(player_id)
    if player:
        return player
    raise HTTPException(status_code=404, detail="Player not found")


# ===== COURT ENDPOINTS =====

@app.get("/api/courts", response_model=List[Court])
async def get_all_courts():
    """Get all basketball courts."""
    return sheets_service.get_all_courts()


@app.get("/api/courts/{court_id}", response_model=Court)
async def get_court_by_id(court_id: str):
    """Get a specific court by ID."""
    court = sheets_service.get_court_by_id(court_id)
    if court:
        return court
    raise HTTPException(status_code=404, detail="Court not found")


# ===== MATCH ENDPOINTS =====

@app.get("/api/matches", response_model=List[Match])
async def get_all_matches():
    """Get all matches."""
    return sheets_service.get_all_matches()


@app.get("/api/matches/open", response_model=List[Match])
async def get_open_matches():
    """Get all open matches."""
    return sheets_service.get_open_matches()


@app.get("/api/matches/{match_id}", response_model=Match)
async def get_match_by_id(match_id: str):
    """Get a specific match by ID."""
    match = sheets_service.get_match_by_id(match_id)
    if match:
        return match
    raise HTTPException(status_code=404, detail="Match not found")


@app.post("/api/matches/{match_id}/join")
async def join_match(match_id: str, player_id: str):
    """Join a match."""
    match = sheets_service.get_match_by_id(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    if match.status != MatchStatus.OPEN:
        raise HTTPException(status_code=400, detail="Match is not open")

    success = sheets_service.join_match(match_id, player_id)
    if success:
        return {"message": "Successfully joined match", "match_id": match_id}
    raise HTTPException(status_code=400, detail="Failed to join match")


@app.post("/api/matches", response_model=Match)
async def create_match(
    court_id: str,
    datetime: str,
    skill_level: SkillLevel,
    created_by: str = None,
    max_players: int = 10
):
    """Create a new match."""
    match = Match(
        court_id=court_id,
        datetime=datetime,
        skill_level=skill_level,
        max_players=max_players,
        created_by=created_by
    )

    created = sheets_service.create_match(match)
    if created:
        return created
    raise HTTPException(status_code=500, detail="Failed to create match")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
