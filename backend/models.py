from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SkillLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class MatchStatus(str, Enum):
    OPEN = "open"
    FULL = "full"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Court(BaseModel):
    id: str
    name: str
    address: str
    district: str
    price: int
    opening_hours: str
    phone: Optional[str] = None


class Player(BaseModel):
    id: Optional[str] = None
    name: str
    phone: str
    skill_level: SkillLevel
    preferred_district: str
    created_at: Optional[str] = None


class Match(BaseModel):
    id: Optional[str] = None
    court_id: str
    court_name: Optional[str] = None
    datetime: str
    skill_level: SkillLevel
    max_players: int = 10
    current_players: int = 0
    player_ids: List[str] = []
    status: MatchStatus = MatchStatus.OPEN
    created_by: Optional[str] = None


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    player_id: Optional[str] = None
    conversation_history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    response: str
    player_id: Optional[str] = None
    action_result: Optional[dict] = None


class PlayerCreateRequest(BaseModel):
    name: str
    phone: str
    skill_level: SkillLevel
    preferred_district: str
