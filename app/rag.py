import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings


@dataclass
class DocChunk:
    source: str
    text: str


class TfidfRAG:
    def __init__(
        self,
        processed_path: str = "data/processed/chunks.jsonl",
        index_path: str = "data/vector_db/tfidf_index.pkl",
    ) -> None:
        self.processed_path = Path(processed_path)
        self.index_path = Path(index_path)
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix = None
        self.chunks: List[DocChunk] = []

    def load_chunks(self) -> None:
        if not self.processed_path.exists():
            raise FileNotFoundError(
                f"未找到 {self.processed_path}，请先运行 scripts/clean_data.py。"
            )
        self.chunks = []
        with self.processed_path.open("r", encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                self.chunks.append(DocChunk(source=row["source"], text=row["text"]))

    def build_and_save(self) -> None:
        self.load_chunks()
        corpus = [c.text for c in self.chunks]
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.matrix = self.vectorizer.fit_transform(corpus)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with self.index_path.open("wb") as f:
            pickle.dump(
                {"vectorizer": self.vectorizer, "matrix": self.matrix, "chunks": self.chunks},
                f,
            )

    def load_index(self) -> None:
        if not self.index_path.exists():
            raise FileNotFoundError(
                f"未找到 {self.index_path}，请先运行 scripts/build_kb.py。"
            )
        with self.index_path.open("rb") as f:
            data = pickle.load(f)
        self.vectorizer = data["vectorizer"]
        self.matrix = data["matrix"]
        self.chunks = data["chunks"]

    def retrieve(self, question: str, top_k: int | None = None) -> List[DocChunk]:
        if self.vectorizer is None or self.matrix is None:
            self.load_index()

        k = top_k or settings.top_k
        q_vec = self.vectorizer.transform([question])
        sims = cosine_similarity(q_vec, self.matrix).flatten()
        idxs = sims.argsort()[::-1][:k]
        return [self.chunks[i] for i in idxs]

    @staticmethod
    def format_context(chunks: List[DocChunk]) -> str:
        if not chunks:
            return "（未检索到相关资料）"
        parts = []
        for i, c in enumerate(chunks, start=1):
            parts.append(f"[资料{i} | 来源:{c.source}]\n{c.text}")
        return "\n\n".join(parts)
