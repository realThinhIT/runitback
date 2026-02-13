"""
Seed demo data into Google Sheets for a new RunItBackHanoi project.

Usage:
    python seed_demo_data.py

This script will:
1. Create the Courts, Players, and Matches tabs (if they don't exist)
2. Clear any existing data in those tabs
3. Populate them with headers and demo data

Requires:
    - GOOGLE_SHEETS_ID set in .env
    - GOOGLE_CREDENTIALS_PATH set in .env (defaults to ./credentials.json)
"""

import os
import sys
from datetime import datetime, timedelta

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials.json")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Sheet tab names
COURTS_SHEET = "Courts"
PLAYERS_SHEET = "Players"
MATCHES_SHEET = "Matches"

# ── Headers ──────────────────────────────────────────────────────────────────

COURTS_HEADERS = ["id", "name", "address", "district", "price", "opening_hours", "phone"]
PLAYERS_HEADERS = ["id", "name", "phone", "skill_level", "preferred_district", "created_at"]
MATCHES_HEADERS = [
    "id", "court_id", "court_name", "datetime", "skill_level",
    "max_players", "current_players", "player_ids", "status", "created_by",
]

# ── Demo data ────────────────────────────────────────────────────────────────

COURTS_DATA = [
    ["C001", "Sân Vạn Phúc Sports Center", "73 Vạn Bảo", "Ba Đình", 150000, "6:00-22:00", "024-1234-5678"],
    ["C002", "Sân Đại học Kiến Trúc", "Nguyễn Trãi", "Thanh Xuân", 0, "6:00-21:00", ""],
    ["C003", "Sân Đại học Y Hà Nội", "Tôn Thất Tùng", "Đống Đa", 0, "6:00-21:00", ""],
    ["C004", "Sân New Quarter Basketball", "Ngõ 612 Hoàng Hoa Thám", "Ba Đình", 200000, "6:00-22:00", ""],
    ["C005", "Sân Mỹ Đình", "Phường Nhân Mỹ", "Nam Từ Liêm", 100000, "6:00-22:00", ""],
    ["C006", "Sân Nguyễn Thị Thập", "Nguyễn Thị Thập", "Cầu Giấy", 120000, "6:00-22:00", ""],
    ["C007", "Sân SkyTrap Basketball", "1 Trịnh Văn Bô", "Nam Từ Liêm", 180000, "7:00-22:00", ""],
    ["C008", "Sân Level Basketball", "Tòa nhà The Nine", "Cầu Giấy", 200000, "8:00-22:00", ""],
    ["C009", "Sân vận động Bách Khoa", "Lê Thanh Nghị", "Hai Bà Trưng", 80000, "6:00-21:00", ""],
    ["C010", "Sân trường Chu Văn An", "Thụy Khuê", "Tây Hồ", 0, "17:00-20:00", ""],
    ["C011", "Sân trường Hà Nội - Amsterdam", "Nam Cao", "Cầu Giấy", 0, "17:00-20:00", ""],
    ["C012", "Sân Đại học Sư Phạm", "80 Trần Quốc Hoàn", "Cầu Giấy", 0, "6:00-21:00", ""],
]

now = datetime.now()


def _ts(days_offset: int = 0) -> str:
    """Return a timestamp string offset by days from now."""
    return (now + timedelta(days=days_offset)).strftime("%Y-%m-%d %H:%M:%S")


PLAYERS_DATA = [
    ["P001", "Nguyễn Văn An", "0901234001", "Intermediate", "Ba Đình", _ts(-10)],
    ["P002", "Trần Minh Đức", "0901234002", "Advanced", "Cầu Giấy", _ts(-9)],
    ["P003", "Lê Hoàng Nam", "0901234003", "Intermediate", "Đống Đa", _ts(-8)],
    ["P004", "Phạm Quốc Bảo", "0901234004", "Beginner", "Thanh Xuân", _ts(-7)],
    ["P005", "Hoàng Tuấn Kiệt", "0901234005", "Advanced", "Cầu Giấy", _ts(-6)],
    ["P006", "Vũ Đình Hùng", "0901234006", "Advanced", "Nam Từ Liêm", _ts(-5)],
    ["P007", "Đỗ Quang Hải", "0901234007", "Intermediate", "Hai Bà Trưng", _ts(-4)],
    ["P008", "Ngô Thanh Tùng", "0901234008", "Beginner", "Tây Hồ", _ts(-3)],
    ["P009", "Bùi Công Vinh", "0901234009", "Intermediate", "Ba Đình", _ts(-2)],
    ["P010", "Dương Anh Quân", "0901234010", "Advanced", "Cầu Giấy", _ts(-1)],
    ["P011", "Trịnh Đức Long", "0901234011", "Beginner", "Đống Đa", _ts(-1)],
    ["P012", "Mai Xuân Trường", "0901234012", "Beginner", "Thanh Xuân", _ts(0)],
]

# Generate match datetimes a few days in the future so they look upcoming
MATCHES_DATA = [
    [
        "M001", "C006", "Sân Nguyễn Thị Thập",
        (now + timedelta(days=1)).strftime("%Y-%m-%d") + " 19:00",
        "Intermediate", 10, 4, "P001,P003,P007,P009", "open", "P001",
    ],
    [
        "M002", "C008", "Sân Level Basketball",
        (now + timedelta(days=1)).strftime("%Y-%m-%d") + " 20:00",
        "Advanced", 10, 6, "P002,P005,P006,P010,P003,P007", "open", "P002",
    ],
    [
        "M003", "C001", "Sân Vạn Phúc Sports Center",
        (now + timedelta(days=2)).strftime("%Y-%m-%d") + " 18:00",
        "Beginner", 10, 2, "P004,P008", "open", "P004",
    ],
    [
        "M004", "C009", "Sân vận động Bách Khoa",
        (now + timedelta(days=3)).strftime("%Y-%m-%d") + " 17:30",
        "Intermediate", 10, 3, "P001,P007,P012", "open", "P007",
    ],
    [
        "M005", "C005", "Sân Mỹ Đình",
        (now + timedelta(days=4)).strftime("%Y-%m-%d") + " 19:00",
        "Advanced", 10, 5, "P002,P005,P006,P010,P009", "open", "P006",
    ],
]

# ── Helpers ──────────────────────────────────────────────────────────────────


def get_service():
    """Build and return an authorized Google Sheets API service."""
    if not SPREADSHEET_ID:
        print("Error: GOOGLE_SHEETS_ID is not set in .env")
        sys.exit(1)
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"Error: Credentials file not found at {CREDENTIALS_PATH}")
        sys.exit(1)

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=credentials)


def ensure_sheets_exist(service):
    """Create the Courts, Players, and Matches tabs if they don't exist."""
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    existing_titles = {s["properties"]["title"] for s in spreadsheet["sheets"]}

    requests = []
    for title in [COURTS_SHEET, PLAYERS_SHEET, MATCHES_SHEET]:
        if title not in existing_titles:
            requests.append({"addSheet": {"properties": {"title": title}}})
            print(f"  Creating sheet tab: {title}")

    if requests:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID, body={"requests": requests}
        ).execute()
    else:
        print("  All sheet tabs already exist.")


def clear_and_write(service, sheet_name: str, headers: list, rows: list):
    """Clear a sheet tab then write headers + data rows."""
    range_all = f"{sheet_name}!A:Z"
    # Clear
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID, range=range_all, body={}
    ).execute()

    # Write headers + data
    values = [headers] + rows
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()
    print(f"  {sheet_name}: wrote {len(rows)} rows")


# ── Main ─────────────────────────────────────────────────────────────────────


def seed():
    print("RunItBackHanoi - Seed Demo Data")
    print("=" * 40)

    print("\nConnecting to Google Sheets API...")
    service = get_service()

    print("\nEnsuring sheet tabs exist...")
    ensure_sheets_exist(service)

    print("\nWriting demo data...")
    clear_and_write(service, COURTS_SHEET, COURTS_HEADERS, COURTS_DATA)
    clear_and_write(service, PLAYERS_SHEET, PLAYERS_HEADERS, PLAYERS_DATA)
    clear_and_write(service, MATCHES_SHEET, MATCHES_HEADERS, MATCHES_DATA)

    print(f"\nDone! Spreadsheet ID: {SPREADSHEET_ID}")
    print(f"Open: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")


if __name__ == "__main__":
    seed()
