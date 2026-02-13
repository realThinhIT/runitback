import os
from openai import OpenAI
from typing import List, Optional
from models import Court, Match, Player, ChatMessage


class OpenAIService:
    def __init__(self):
        # Support multiple API providers
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")  # For OpenRouter or other providers

        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)

        # Model can be configured via env (useful for OpenRouter)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def _build_system_prompt(self, courts: List[Court], matches: List[Match], player: Player = None) -> str:
        """Build the system prompt with current data."""

        # Format courts data
        courts_text = "\n".join([
            f"- {c.name} (ID: {c.id}): {c.address}, {c.district}. "
            f"Giá: {c.price:,}đ/giờ. Giờ mở cửa: {c.opening_hours}"
            for c in courts
        ])

        # Format matches data
        if matches:
            matches_text = "\n".join([
                f"- Trận #{m.id}: Sân {m.court_name} ({m.court_id}), "
                f"Thời gian: {m.datetime}, Trình độ: {m.skill_level.value}, "
                f"Còn {m.max_players - m.current_players}/{m.max_players} chỗ trống, "
                f"Người chơi đã đăng ký: {', '.join(m.player_ids) if m.player_ids else 'chưa có'}"
                for m in matches
            ])
        else:
            matches_text = "Hiện tại chưa có trận đấu nào đang mở."

        # Player context
        player_context = ""
        if player:
            # Find matches this player has registered for
            registered_matches = [m for m in matches if player.id in m.player_ids] if matches else []
            if registered_matches:
                registered_text = ", ".join([f"#{m.id} ({m.court_name}, {m.datetime})" for m in registered_matches])
            else:
                registered_text = "Chưa đăng ký trận nào"

            player_context = f"""
## Thông tin người chơi hiện tại:
- Tên: {player.name}
- ID: {player.id}
- Trình độ: {player.skill_level.value}
- Khu vực ưa thích: {player.preferred_district}
- Các trận đã đăng ký: {registered_text}
"""

        system_prompt = f"""Bạn là trợ lý AI của RunItBackHanoi - nền tảng ghép trận bóng rổ tại Hà Nội.

## Vai trò của bạn:
- Giúp người chơi tìm trận đấu phù hợp với trình độ và khu vực
- Hỗ trợ đăng ký tham gia trận
- Tạo trận đấu mới
- Cung cấp thông tin sân bóng rổ

## Dữ liệu sân bóng rổ hiện có:
{courts_text}

## Các trận đấu đang mở:
{matches_text}
{player_context}
## Quy tắc ghép trận:
1. Ưu tiên ghép theo trình độ tương đương (Beginner/Intermediate/Advanced)
2. Ưu tiên sân gần khu vực người chơi
3. Kiểm tra thời gian phù hợp
4. Nếu không có trận phù hợp, gợi ý tạo trận mới

## Trình độ:
- Beginner: Mới chơi, đang học cơ bản
- Intermediate: Chơi được, hiểu chiến thuật cơ bản
- Advanced: Chơi tốt, thi đấu thường xuyên

## Các quận/huyện Hà Nội:
Ba Đình, Hoàn Kiếm, Hai Bà Trưng, Đống Đa, Cầu Giấy, Thanh Xuân, Hoàng Mai, Long Biên, Tây Hồ, Nam Từ Liêm, Bắc Từ Liêm, Hà Đông

## Cách trả lời:
- Dùng tiếng Việt có dấu, thân thiện, ngắn gọn
- Luôn đưa ra gợi ý cụ thể dựa trên dữ liệu
- Khi người dùng muốn tham gia trận, xác nhận lại thông tin trận đó
- Khi người dùng muốn tạo trận mới, hỏi: sân nào, thời gian nào, trình độ nào
- Nếu thiếu thông tin (trình độ, khu vực, thời gian), hãy hỏi thêm

## Hành động đặc biệt (RẤT QUAN TRỌNG):
Khi người dùng xác nhận một hành động, bạn PHẢI thêm một khối ACTION ở CUỐI phản hồi. Khối này sẽ được hệ thống xử lý tự động và không hiển thị cho người dùng.

### Tham gia trận:
Khi người dùng xác nhận muốn tham gia trận, trả lời thân thiện rồi thêm:
[ACTION:{{"type":"join_match","match_id":"M001"}}]

### Tạo trận mới:
Khi người dùng đã cung cấp đủ thông tin (sân, thời gian, trình độ) và xác nhận tạo trận, trả lời thân thiện rồi thêm:
[ACTION:{{"type":"create_match","court_id":"C001","datetime":"2025-02-15 19:00","skill_level":"Intermediate","max_players":10}}]

### Rời trận:
Khi người dùng muốn rời/hủy tham gia trận:
[ACTION:{{"type":"leave_match","match_id":"M001"}}]

### Cập nhật thông tin:
Khi người dùng muốn thay đổi thông tin cá nhân (trình độ, khu vực):
[ACTION:{{"type":"update_player","skill_level":"Advanced","preferred_district":"Cầu Giấy"}}]

Quy tắc:
- CHỈ thêm ACTION khi người dùng ĐÃ XÁC NHẬN rõ ràng (không thêm khi đang hỏi/tư vấn)
- Luôn đặt ACTION ở dòng cuối cùng của phản hồi
- Phần text phản hồi phía trên vẫn viết tiếng Việt thân thiện bình thường
- JSON trong ACTION phải hợp lệ
"""
        return system_prompt

    def chat(self, message: str, courts: List[Court], matches: List[Match], player: Player = None, conversation_history: List[ChatMessage] = None) -> str:
        """Send a message to the AI and get a response."""
        try:
            system_prompt = self._build_system_prompt(courts, matches, player)

            messages = [{"role": "system", "content": system_prompt}]

            # Add conversation history for context
            if conversation_history:
                for msg in conversation_history:
                    messages.append({"role": msg.role, "content": msg.content})

            # Add the current user message
            messages.append({"role": "user", "content": message})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return f"Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau. (Error: {str(e)})"


class DemoOpenAIService(OpenAIService):
    """Demo service for testing without OpenAI API."""

    def __init__(self):
        self.client = None
        self.model = "demo"

    def chat(self, message: str, courts: List[Court], matches: List[Match], player: Player = None, conversation_history: List[ChatMessage] = None) -> str:
        """Return demo responses based on keywords."""
        message_lower = message.lower()

        # Check for match search
        if any(word in message_lower for word in ["tìm", "chơi", "trận", "match", "game", "tối", "sáng", "chiều"]):
            if matches:
                match_list = "\n".join([
                    f"- Trận #{m.id}: Sân {m.court_name}, {m.datetime}, "
                    f"trình độ {m.skill_level.value}, còn {m.max_players - m.current_players} chỗ"
                    for m in matches[:3]
                ])
                return f"Hiện có {len(matches)} trận đang mở:\n{match_list}\n\nBạn muốn tham gia trận nào?"
            return "Hiện chưa có trận nào đang mở. Bạn có muốn tạo trận mới không?"

        # Check for court info
        if any(word in message_lower for word in ["sân", "court", "địa chỉ", "address", "ở đâu"]):
            court_list = "\n".join([
                f"- {c.name}: {c.address}, {c.district}. Giá: {c.price:,}đ/h"
                for c in courts[:5]
            ])
            return f"Một số sân bóng rổ tại Hà Nội:\n{court_list}"

        # Check for join request
        if any(word in message_lower for word in ["tham gia", "join", "đăng ký", "register", "vào"]):
            if matches:
                return f"Bạn muốn tham gia trận nào? Hiện có trận #{matches[0].id} tại {matches[0].court_name} đang mở."
            return "Hiện chưa có trận nào. Bạn có muốn tạo trận mới không?"

        # Default response
        return """Xin chào! Tôi là trợ lý RunItBackHanoi. Tôi có thể giúp bạn:
- Tìm trận đấu phù hợp
- Tham gia trận đấu
- Tạo trận mới
- Tra cứu thông tin sân

Bạn cần gì hôm nay?"""


def get_openai_service() -> OpenAIService:
    """Factory function to get the appropriate OpenAI service."""
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        return OpenAIService()
    else:
        print("Using demo AI responses (OpenAI API not configured)")
        return DemoOpenAIService()
