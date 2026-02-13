import os
import json
import tempfile
from typing import List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from models import Court, Player, Match, SkillLevel, MatchStatus
from datetime import datetime


class SheetsService:
    def __init__(self):
        self.spreadsheet_id = os.getenv("GOOGLE_SHEETS_ID")
        self.credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials.json")
        self.service = None
        self._initialize_service()

    def _initialize_service(self):
        """Initialize Google Sheets API service."""
        try:
            # Support credentials from env var (for cloud deployment) or file
            credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
            if credentials_json:
                info = json.loads(credentials_json)
                credentials = service_account.Credentials.from_service_account_info(
                    info,
                    scopes=["https://www.googleapis.com/auth/spreadsheets"]
                )
            else:
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=["https://www.googleapis.com/auth/spreadsheets"]
                )
            self.service = build("sheets", "v4", credentials=credentials)
        except Exception as e:
            print(f"Warning: Could not initialize Google Sheets service: {e}")
            self.service = None

    def _get_sheet_data(self, range_name: str) -> List[List[str]]:
        """Get data from a sheet range."""
        if not self.service:
            return []
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            return result.get("values", [])
        except Exception as e:
            print(f"Error reading from sheet: {e}")
            return []

    def _append_row(self, range_name: str, values: List) -> bool:
        """Append a row to a sheet."""
        if not self.service:
            return False
        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body={"values": [values]}
            ).execute()
            return True
        except Exception as e:
            print(f"Error appending to sheet: {e}")
            return False

    def _update_cell(self, range_name: str, value: str) -> bool:
        """Update a specific cell."""
        if not self.service:
            return False
        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body={"values": [[value]]}
            ).execute()
            return True
        except Exception as e:
            print(f"Error updating cell: {e}")
            return False

    # ===== COURTS =====
    def get_all_courts(self) -> List[Court]:
        """Get all basketball courts."""
        data = self._get_sheet_data("Courts!A2:G100")
        courts = []
        for row in data:
            if len(row) >= 6:
                courts.append(Court(
                    id=row[0],
                    name=row[1],
                    address=row[2],
                    district=row[3],
                    price=int(row[4]) if row[4] else 0,
                    opening_hours=row[5],
                    phone=row[6] if len(row) > 6 else None
                ))
        return courts

    def get_court_by_id(self, court_id: str) -> Optional[Court]:
        """Get a specific court by ID."""
        courts = self.get_all_courts()
        for court in courts:
            if court.id == court_id:
                return court
        return None

    # ===== PLAYERS =====
    def get_all_players(self) -> List[Player]:
        """Get all registered players."""
        data = self._get_sheet_data("Players!A2:F100")
        players = []
        for row in data:
            if len(row) >= 5:
                players.append(Player(
                    id=row[0],
                    name=row[1],
                    phone=row[2],
                    skill_level=SkillLevel(row[3]),
                    preferred_district=row[4],
                    created_at=row[5] if len(row) > 5 else None
                ))
        return players

    def get_player_by_phone(self, phone: str) -> Optional[Player]:
        """Get a player by phone number."""
        players = self.get_all_players()
        for player in players:
            if player.phone == phone:
                return player
        return None

    def get_player_by_id(self, player_id: str) -> Optional[Player]:
        """Get a player by ID."""
        players = self.get_all_players()
        for player in players:
            if player.id == player_id:
                return player
        return None

    def create_player(self, player: Player) -> Optional[Player]:
        """Create a new player."""
        # Check if phone already exists
        existing = self.get_player_by_phone(player.phone)
        if existing:
            return existing

        # Generate new ID
        players = self.get_all_players()
        new_id = f"P{len(players) + 1:03d}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        values = [
            new_id,
            player.name,
            player.phone,
            player.skill_level.value,
            player.preferred_district,
            created_at
        ]

        if self._append_row("Players!A:F", values):
            player.id = new_id
            player.created_at = created_at
            return player
        return None

    # ===== MATCHES =====
    def get_all_matches(self) -> List[Match]:
        """Get all matches."""
        data = self._get_sheet_data("Matches!A2:J100")
        matches = []
        for row in data:
            if len(row) >= 8:
                player_ids = row[7].split(",") if len(row) > 7 and row[7] else []
                matches.append(Match(
                    id=row[0],
                    court_id=row[1],
                    court_name=row[2] if len(row) > 2 else None,
                    datetime=row[3],
                    skill_level=SkillLevel(row[4]),
                    max_players=int(row[5]) if row[5] else 10,
                    current_players=int(row[6]) if row[6] else 0,
                    player_ids=[p.strip() for p in player_ids if p.strip()],
                    status=MatchStatus(row[8]) if len(row) > 8 else MatchStatus.OPEN,
                    created_by=row[9] if len(row) > 9 else None
                ))
        return matches

    def get_open_matches(self) -> List[Match]:
        """Get all open matches."""
        matches = self.get_all_matches()
        return [m for m in matches if m.status == MatchStatus.OPEN]

    def get_match_by_id(self, match_id: str) -> Optional[Match]:
        """Get a specific match by ID."""
        matches = self.get_all_matches()
        for match in matches:
            if match.id == match_id:
                return match
        return None

    def create_match(self, match: Match) -> Optional[Match]:
        """Create a new match."""
        matches = self.get_all_matches()
        new_id = f"M{len(matches) + 1:03d}"

        # Get court name
        court = self.get_court_by_id(match.court_id)
        court_name = court.name if court else ""

        values = [
            new_id,
            match.court_id,
            court_name,
            match.datetime,
            match.skill_level.value,
            match.max_players,
            match.current_players,
            ",".join(match.player_ids),
            match.status.value,
            match.created_by or ""
        ]

        if self._append_row("Matches!A:J", values):
            match.id = new_id
            match.court_name = court_name
            return match
        return None

    def join_match(self, match_id: str, player_id: str) -> bool:
        """Add a player to a match."""
        matches = self.get_all_matches()
        for i, match in enumerate(matches):
            if match.id == match_id:
                if player_id in match.player_ids:
                    return True  # Already joined
                if match.current_players >= match.max_players:
                    return False  # Match is full

                # Update player_ids
                new_player_ids = match.player_ids + [player_id]
                row_num = i + 2  # +2 because of header and 0-indexing

                # Update current_players count
                self._update_cell(f"Matches!G{row_num}", str(len(new_player_ids)))
                # Update player_ids list
                self._update_cell(f"Matches!H{row_num}", ",".join(new_player_ids))

                # Update status if full
                if len(new_player_ids) >= match.max_players:
                    self._update_cell(f"Matches!I{row_num}", MatchStatus.FULL.value)

                return True
        return False

    def leave_match(self, match_id: str, player_id: str) -> bool:
        """Remove a player from a match."""
        matches = self.get_all_matches()
        for i, match in enumerate(matches):
            if match.id == match_id:
                if player_id not in match.player_ids:
                    return True  # Not in match, nothing to do
                new_player_ids = [p for p in match.player_ids if p != player_id]
                row_num = i + 2

                self._update_cell(f"Matches!G{row_num}", str(len(new_player_ids)))
                self._update_cell(f"Matches!H{row_num}", ",".join(new_player_ids))

                # Reopen match if it was full
                if match.status == MatchStatus.FULL and len(new_player_ids) < match.max_players:
                    self._update_cell(f"Matches!I{row_num}", MatchStatus.OPEN.value)

                return True
        return False

    def update_player(self, player_id: str, **fields) -> bool:
        """Update player fields in Sheets."""
        players = self.get_all_players()
        # Column mapping: A=id, B=name, C=phone, D=skill_level, E=preferred_district, F=created_at
        field_columns = {
            "name": "B",
            "phone": "C",
            "skill_level": "D",
            "preferred_district": "E",
        }
        for i, player in enumerate(players):
            if player.id == player_id:
                row_num = i + 2
                for field_name, value in fields.items():
                    col = field_columns.get(field_name)
                    if col:
                        self._update_cell(f"Players!{col}{row_num}", str(value))
                return True
        return False


# Demo data for when Google Sheets is not configured
class DemoSheetsService(SheetsService):
    """Demo service with in-memory data for testing without Google Sheets."""

    def __init__(self):
        self.service = None
        self._courts = [
            Court(id="C001", name="Sân Vạn Phúc Sports Center", address="73 Vạn Bảo", district="Ba Đình", price=150000, opening_hours="6:00-22:00", phone="024-1234-5678"),
            Court(id="C002", name="Sân Đại học Kiến Trúc", address="Nguyễn Trãi", district="Thanh Xuân", price=0, opening_hours="6:00-21:00"),
            Court(id="C003", name="Sân Đại học Y Hà Nội", address="Tôn Thất Tùng", district="Đống Đa", price=0, opening_hours="6:00-21:00"),
            Court(id="C004", name="Sân New Quarter Basketball", address="Ngõ 612 Hoàng Hoa Thám", district="Ba Đình", price=200000, opening_hours="6:00-22:00"),
            Court(id="C005", name="Sân Mỹ Đình", address="Phường Nhân Mỹ", district="Nam Từ Liêm", price=100000, opening_hours="6:00-22:00"),
            Court(id="C006", name="Sân Nguyễn Thị Thập", address="Nguyễn Thị Thập", district="Cầu Giấy", price=120000, opening_hours="6:00-22:00"),
            Court(id="C007", name="Sân SkyTrap Basketball", address="1 Trịnh Văn Bô", district="Nam Từ Liêm", price=180000, opening_hours="7:00-22:00"),
            Court(id="C008", name="Sân Level Basketball", address="Tòa nhà The Nine", district="Cầu Giấy", price=200000, opening_hours="8:00-22:00"),
            Court(id="C009", name="Sân vận động Bách Khoa", address="Lê Thanh Nghị", district="Hai Bà Trưng", price=80000, opening_hours="6:00-21:00"),
            Court(id="C010", name="Sân trường Chu Văn An", address="Thụy Khuê", district="Tây Hồ", price=0, opening_hours="17:00-20:00"),
            Court(id="C011", name="Sân trường Hà Nội - Amsterdam", address="Nam Cao", district="Cầu Giấy", price=0, opening_hours="17:00-20:00"),
            Court(id="C012", name="Sân Đại học Sư Phạm", address="80 Trần Quốc Hoàn", district="Cầu Giấy", price=0, opening_hours="6:00-21:00"),
        ]
        self._players: List[Player] = []
        self._matches = [
            Match(id="M001", court_id="C006", court_name="Sân Nguyễn Thị Thập", datetime="2025-02-10 19:00", skill_level=SkillLevel.INTERMEDIATE, max_players=10, current_players=4, player_ids=["P001", "P002", "P003", "P004"], status=MatchStatus.OPEN),
            Match(id="M002", court_id="C008", court_name="Sân Level Basketball", datetime="2025-02-10 20:00", skill_level=SkillLevel.ADVANCED, max_players=10, current_players=6, player_ids=["P005", "P006", "P007", "P008", "P009", "P010"], status=MatchStatus.OPEN),
            Match(id="M003", court_id="C001", court_name="Sân Vạn Phúc Sports Center", datetime="2025-02-11 18:00", skill_level=SkillLevel.BEGINNER, max_players=10, current_players=2, player_ids=["P011", "P012"], status=MatchStatus.OPEN),
        ]

    def get_all_courts(self) -> List[Court]:
        return self._courts

    def get_court_by_id(self, court_id: str) -> Optional[Court]:
        for court in self._courts:
            if court.id == court_id:
                return court
        return None

    def get_all_players(self) -> List[Player]:
        return self._players

    def get_player_by_phone(self, phone: str) -> Optional[Player]:
        for player in self._players:
            if player.phone == phone:
                return player
        return None

    def get_player_by_id(self, player_id: str) -> Optional[Player]:
        for player in self._players:
            if player.id == player_id:
                return player
        return None

    def create_player(self, player: Player) -> Optional[Player]:
        existing = self.get_player_by_phone(player.phone)
        if existing:
            return existing

        new_id = f"P{len(self._players) + 1:03d}"
        player.id = new_id
        player.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._players.append(player)
        return player

    def get_all_matches(self) -> List[Match]:
        return self._matches

    def get_open_matches(self) -> List[Match]:
        return [m for m in self._matches if m.status == MatchStatus.OPEN]

    def get_match_by_id(self, match_id: str) -> Optional[Match]:
        for match in self._matches:
            if match.id == match_id:
                return match
        return None

    def create_match(self, match: Match) -> Optional[Match]:
        new_id = f"M{len(self._matches) + 1:03d}"
        court = self.get_court_by_id(match.court_id)
        match.id = new_id
        match.court_name = court.name if court else ""
        self._matches.append(match)
        return match

    def join_match(self, match_id: str, player_id: str) -> bool:
        for match in self._matches:
            if match.id == match_id:
                if player_id in match.player_ids:
                    return True
                if match.current_players >= match.max_players:
                    return False
                match.player_ids.append(player_id)
                match.current_players = len(match.player_ids)
                if match.current_players >= match.max_players:
                    match.status = MatchStatus.FULL
                return True
        return False

    def leave_match(self, match_id: str, player_id: str) -> bool:
        for match in self._matches:
            if match.id == match_id:
                if player_id not in match.player_ids:
                    return True
                match.player_ids.remove(player_id)
                match.current_players = len(match.player_ids)
                if match.status == MatchStatus.FULL and match.current_players < match.max_players:
                    match.status = MatchStatus.OPEN
                return True
        return False

    def update_player(self, player_id: str, **fields) -> bool:
        for player in self._players:
            if player.id == player_id:
                for field_name, value in fields.items():
                    if hasattr(player, field_name):
                        setattr(player, field_name, value)
                return True
        return False


def get_sheets_service() -> SheetsService:
    """Factory function to get the appropriate sheets service."""
    sheets_id = os.getenv("GOOGLE_SHEETS_ID")
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials.json")

    if sheets_id and (credentials_json or os.path.exists(credentials_path)):
        return SheetsService()
    else:
        print("Using demo data (Google Sheets not configured)")
        return DemoSheetsService()
