import streamlit as st
import requests

st.set_page_config(
    page_title="KPL赛事智能问答Agent",
    layout="wide"
)

st.title("KPL 王者荣耀赛事智能问答 Agent")
st.caption("第一阶段：前后端联调测试版")

query = st.text_input(
    "请输入你的 KPL 问题：",
    placeholder="例如：KPL全局BP是什么意思？"
)

if st.button("提交问题"):
    if not query.strip():
        st.warning("请先输入问题")
    else:
        with st.spinner("正在请求后端接口..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"query": query},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()

                    st.subheader("智能回答")
                    st.write(data.get("answer", ""))

                    st.subheader("问题意图")
                    st.write(data.get("intent", "未知"))

                    st.subheader("参考来源")
                    sources = data.get("sources", [])

                    if sources:
                        for idx, source in enumerate(sources, 1):
                            with st.expander(f"来源 {idx}：{source.get('title', '未知标题')}"):
                                st.write("来源：", source.get("source", "未知来源"))
                                st.write("片段：", source.get("content_preview", "暂无片段"))
                    else:
                        st.info("暂无参考来源")

                else:
                    st.error(f"请求失败，状态码：{response.status_code}")
                    st.write(response.text)

            except requests.exceptions.ConnectionError:
                st.error("连接后端失败，请确认 FastAPI 后端是否已经启动。")

            except Exception as e:
                st.error(f"发生错误：{e}")