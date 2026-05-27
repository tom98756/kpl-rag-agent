'''
数据清洗脚本
'''

import json
from pathlib import Path

from app.config import settings


RAW_DIR = Path("data/raw")
OUT_FILE = Path("data/processed/chunks.jsonl")


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    files = list(RAW_DIR.glob("*.txt")) + list(RAW_DIR.glob("*.md"))
    if not files:
        print("data/raw 下没有 txt 或 md 文件。")
        return

    total = 0
    with OUT_FILE.open("w", encoding="utf-8") as f:
        for file in files:
            text = file.read_text(encoding="utf-8", errors="ignore")
            chunks = split_text(text, settings.chunk_size, settings.chunk_overlap)
            for c in chunks:
                row = {"source": file.name, "text": c}
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                total += 1

    print(f"完成清洗，共生成 {total} 个分块，输出：{OUT_FILE}")


if __name__ == "__main__":
    main()
