'''
测试检索脚本
'''

from app.rag import TfidfRAG


def main() -> None:
    rag = TfidfRAG()
    q = "KPL 战队常见运营思路是什么？"
    chunks = rag.retrieve(q, top_k=3)
    print("问题：", q)
    print(rag.format_context(chunks))


if __name__ == "__main__":
    main()
