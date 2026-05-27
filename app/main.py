from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="KPL赛事智能问答Agent")


class ChatRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {
        "message": "KPL赛事智能问答Agent后端服务已启动"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    user_query = request.query

    return {
        "answer": f"后端已收到你的问题：{user_query}",
        "intent": "test_intent",
        "sources": [
            {
                "title": "测试来源",
                "source": "本地测试数据",
                "content_preview": "这里是测试阶段的模拟参考资料。"
            }
        ]
    }