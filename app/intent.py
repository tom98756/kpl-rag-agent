'''
判断用户问题属于哪种类型
'''



from enum import Enum


class Intent(str, Enum):
    KPL_QA = "kpl_qa"
    SMALL_TALK = "small_talk"
    MEMORY_QUERY = "memory_query"


KPL_KEYWORDS = [
    "kpl",
    "王者荣耀",
    "战队",
    "选手",
    "比赛",
    "赛季",
    "季后赛",
    "总决赛",
    "bp",
    "阵容",
]

MEMORY_KEYWORDS = ["你记得", "刚才", "上次", "我之前说", "你还记得"]


def detect_intent(user_text: str) -> Intent:
    text = user_text.lower()
    if any(k in user_text for k in MEMORY_KEYWORDS):
        return Intent.MEMORY_QUERY
    if any(k in text for k in KPL_KEYWORDS):
        return Intent.KPL_QA
    return Intent.SMALL_TALK
