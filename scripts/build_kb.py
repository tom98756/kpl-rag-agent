'''
构建知识库脚本
'''

from app.rag import TfidfRAG


def main() -> None:
    rag = TfidfRAG()
    rag.build_and_save()
    print("知识库构建完成：data/vector_db/tfidf_index.pkl")


if __name__ == "__main__":
    main()
