import json
import re
from pathlib import Path


RAW_DATA_PATH = Path("data/raw/kpl_raw.json")
PROCESSED_DATA_PATH = Path("data/processed/kpl_docs.json")


VALID_TYPES = {
    "rule",
    "team",
    "player",
    "match",
    "award",
    "bp",
    "term",
    "general"
}


def clean_text(text: str) -> str:
    """
    清洗正文文本：
    1. 去掉首尾空格
    2. 合并多个空格
    3. 合并多个换行
    4. 删除制表符
    """
    if not isinstance(text, str):
        return ""

    text = text.replace("\t", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


def normalize_type(doc_type: str) -> str:
    """
    统一 type 字段。
    如果 type 不在合法范围内，统一设置为 general。
    """
    if not isinstance(doc_type, str):
        return "general"

    doc_type = doc_type.strip().lower()

    type_map = {
        "规则": "rule",
        "赛制": "rule",
        "rule": "rule",

        "战队": "team",
        "队伍": "team",
        "team": "team",

        "选手": "player",
        "player": "player",

        "比赛": "match",
        "赛事": "match",
        "match": "match",

        "奖项": "award",
        "荣誉": "award",
        "award": "award",

        "bp": "bp",
        "英雄": "bp",
        "阵容": "bp",

        "术语": "term",
        "term": "term",

        "通用": "general",
        "general": "general"
    }

    return type_map.get(doc_type, "general")


def normalize_season(season: str) -> str:
    """
    统一 season 字段。
    为空时设置为“通用”。
    """
    if not isinstance(season, str):
        return "通用"

    season = season.strip()

    if not season:
        return "通用"

    return season


def normalize_keywords(keywords):
    """
    统一 keywords 字段。
    支持 list 或字符串，最终统一成 list[str]。
    """
    if keywords is None:
        return []

    if isinstance(keywords, list):
        return [str(k).strip() for k in keywords if str(k).strip()]

    if isinstance(keywords, str):
        keywords = keywords.replace("，", ",")
        return [k.strip() for k in keywords.split(",") if k.strip()]

    return []


def is_valid_doc(doc: dict) -> bool:
    """
    判断一条数据是否有效。
    至少要求 title 和 content 不为空。
    """
    title = clean_text(doc.get("title", ""))
    content = clean_text(doc.get("content", ""))

    if not title:
        return False

    if not content:
        return False

    return True


def remove_duplicates(docs):
    """
    去重逻辑：
    使用 title + content 前 50 个字符作为去重 key。
    """
    seen = set()
    unique_docs = []

    for doc in docs:
        key = doc["title"] + "_" + doc["content"][:50]

        if key not in seen:
            seen.add(key)
            unique_docs.append(doc)

    return unique_docs


def load_raw_data():
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"未找到原始数据文件：{RAW_DATA_PATH}")

    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("kpl_raw.json 最外层必须是数组 []")

    return data


def save_processed_data(docs):
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(PROCESSED_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)


def main():
    raw_docs = load_raw_data()

    processed_docs = []
    skipped_count = 0

    for idx, doc in enumerate(raw_docs, start=1):
        if not isinstance(doc, dict):
            skipped_count += 1
            continue

        if not is_valid_doc(doc):
            skipped_count += 1
            continue

        doc_type = normalize_type(doc.get("type", "general"))

        processed_doc = {
            "id": f"kpl_{idx:04d}",
            "title": clean_text(doc.get("title", "")),
            "type": doc_type,
            "season": normalize_season(doc.get("season", "通用")),
            "content": clean_text(doc.get("content", "")),
            "source": clean_text(doc.get("source", "未知来源")),
            "keywords": normalize_keywords(doc.get("keywords", []))
        }

        processed_docs.append(processed_doc)

    before_dedup = len(processed_docs)
    processed_docs = remove_duplicates(processed_docs)
    after_dedup = len(processed_docs)

    save_processed_data(processed_docs)

    print("数据清洗完成")
    print(f"原始数据数量：{len(raw_docs)}")
    print(f"跳过无效数据：{skipped_count}")
    print(f"去重前数量：{before_dedup}")
    print(f"去重后数量：{after_dedup}")
    print(f"输出文件：{PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    main()