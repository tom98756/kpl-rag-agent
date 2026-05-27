# KPL RAG Agent

一个面向 **KPL 赛事问答** 的初学者友好 Agent 框架，包含：

- 基础 RAG 检索
- 意图识别（赛事问答 / 闲聊 / 记忆提取）
- 对话短期记忆
- CLI 交互入口
- Streamlit Web 页面

## 1. 安装

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. 配置环境变量

```bash
copy .env.example .env
```

填写 `.env` 里的 `OPENAI_API_KEY`。

## 3. 准备数据

把你的 KPL 资料（txt / md）放到 `data/raw/` 下。

## 4. 构建知识库

```bash
python scripts/clean_data.py
python scripts/build_kb.py
```

## 5. 运行命令行问答

```bash
python -m app.main
```

## 6. 运行 Web 页面

```bash
streamlit run web/streamlit_app.py
```

---

## 项目结构

- `app/`：核心逻辑（配置、RAG、意图、记忆、LLM）
- `scripts/`：数据预处理、索引构建、测试脚本
- `data/`：原始数据、处理后数据、向量库
- `web/`：Streamlit 页面
- `docs/`：开发计划文档
