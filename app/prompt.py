'''
把用户问题、检索资料、历史对话拼成大模型看的提示词
prompt.py = 告诉大模型应该怎么回答
'''

SYSTEM_PROMPT = """你是 KPL 赛事问答助手。
请基于已提供的检索内容回答，要求：
1) 优先给出结论，再给简短依据；
2) 若检索内容不足，明确说“资料不足”，并给出可补充的信息方向；
3) 不要编造不存在的赛况、选手数据或时间线。"""


def build_user_prompt(question: str, context: str, history: str) -> str:
    return f"""【历史对话】
{history}

【检索资料】
{context}

【用户问题】
{question}

请给出清晰、简洁、专业的回答。"""
