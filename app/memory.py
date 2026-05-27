from collections import defaultdict, deque
from typing import Deque, Dict, List, Tuple


class ConversationMemory:
    def __init__(self, max_turns: int = 6) -> None:
        self._sessions: Dict[str, Deque[Tuple[str, str]]] = defaultdict(
            lambda: deque(maxlen=max_turns)
        )

    def add_turn(self, session_id: str, user_msg: str, assistant_msg: str) -> None:
        self._sessions[session_id].append((user_msg, assistant_msg))

    def get_turns(self, session_id: str) -> List[Tuple[str, str]]:
        return list(self._sessions[session_id])

    def format_history(self, session_id: str) -> str:
        turns = self.get_turns(session_id)
        if not turns:
            return "（暂无历史对话）"
        lines = []
        for user_msg, assistant_msg in turns:
            lines.append(f"用户：{user_msg}")
            lines.append(f"助手：{assistant_msg}")
        return "\n".join(lines)
