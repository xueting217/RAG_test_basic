import time
from rag import RagService
import streamlit as st
import config_data as config

# 标题
st.title("智能客服")
st.divider()            # 分隔符

# 添加Apple风格的自定义样式
st.markdown("""
<style>
/* 全局样式 */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    background-color: #f5f5f7;
    color: #1d1d1f;
    line-height: 1.6;
}

/* 消息气泡样式 */
.user-message {
    background-color: #0071e3;
    color: white;
    padding: 16px 20px;
    border-radius: 18px;
    margin-bottom: 16px;
    max-width: 70%;
    align-self: flex-end;
    margin-left: auto;
    box-shadow: 0 2px 8px rgba(0, 113, 227, 0.2);
    transition: all 0.3s ease;
}

.user-message:hover {
    box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
    transform: translateY(-1px);
}

.ai-message {
    background-color: white;
    color: #1d1d1f;
    padding: 16px 20px;
    border-radius: 18px;
    margin-bottom: 16px;
    max-width: 70%;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.ai-message:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-1px);
}

/* 容器样式 */
.message-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 20px;
    background-color: white;
    border-radius: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

/* 按钮样式 */
.stButton > button {
    background-color: #f5f5f7;
    color: #1d1d1f;
    border: 1px solid #d2d2d7;
    border-radius: 980px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
    outline: none;
}

.stButton > button:hover {
    background-color: #e8e8ed;
    border-color: #d2d2d7;
    transform: translateY(-1px);
}

.stButton > button:active {
    background-color: #d2d2d7;
    transform: translateY(0);
}

/* 输入框样式 */
.stChatInput > div > textarea {
    border: 1px solid #d2d2d7;
    border-radius: 980px;
    padding: 12px 16px;
    font-size: 14px;
    transition: all 0.3s ease;
}

.stChatInput > div > textarea:focus {
    border-color: #0071e3;
    box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.1);
    outline: none;
}

/* 反馈按钮容器 */
.feedback-container {
    display: flex;
    gap: 12px;
    margin-top: 8px;
    margin-bottom: 20px;
    max-width: 70%;
}

.feedback-button {
    flex: 1;
    border-radius: 980px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
}

/* 标题样式 */
h1 {
    font-weight: 600;
    font-size: 32px;
    margin-bottom: 20px;
    color: #1d1d1f;
}

/* 分割线样式 */
hr {
    border: none;
    height: 1px;
    background-color: #d2d2d7;
    margin: 20px 0;
}

/* 加载动画 */
.stSpinner > div {
    border-color: #0071e3;
}

/* 成功和错误消息 */
.stSuccess {
    background-color: rgba(52, 199, 89, 0.1);
    color: #34c759;
    border-radius: 12px;
    padding: 12px;
    margin-top: 8px;
}

.stError {
    background-color: rgba(255, 59, 48, 0.1);
    color: #ff3b30;
    border-radius: 12px;
    padding: 12px;
    margin-top: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .user-message, .ai-message {
        max-width: 85%;
    }
    
    .message-container {
        padding: 16px;
    }
}
</style>
""", unsafe_allow_html=True)

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

if "feedback" not in st.session_state:
    st.session_state["feedback"] = []

# 显示对话历史
message_container = st.container()
with message_container:
    for i, message in enumerate(st.session_state["message"]):
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # 为AI消息添加反馈按钮
        if message["role"] == "assistant" and i > 0:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 有用", key=f"useful_{i}"):
                    st.session_state["feedback"].append({"message_index": i, "feedback": "useful", "content": message["content"]})
                    st.success("感谢您的反馈！")
            with col2:
                if st.button("👎 无用", key=f"useless_{i}"):
                    st.session_state["feedback"].append({"message_index": i, "feedback": "useless", "content": message["content"]})
                    st.error("我们会继续改进！")

# 会话管理
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("清空对话"):
        st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]
        st.session_state["feedback"] = []
        st.rerun()

# 在页面最下方提供用户输入栏
prompt = st.chat_input(placeholder="请输入你的问题...")

if prompt:
    # 在页面输出用户的提问
    st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
    st.session_state["message"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("正在检索知识库..."):
        time.sleep(0.5)  # 模拟检索过程
        with st.spinner("AI生成回答中..."):
            res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)

            def capture(generator, cache_list):
                for chunk in generator:
                    cache_list.append(chunk)
                    yield chunk

            st.markdown('<div class="ai-message">', unsafe_allow_html=True)
            st.write_stream(capture(res_stream, ai_res_list))
            st.markdown('</div>', unsafe_allow_html=True)
            
            ai_response = "".join(ai_res_list)
            st.session_state["message"].append({"role": "assistant", "content": ai_response})
            
            # 为新的AI回答添加反馈按钮
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 有用", key=f"useful_{len(st.session_state['message'])-1}"):
                    st.session_state["feedback"].append({"message_index": len(st.session_state['message'])-1, "feedback": "useful", "content": ai_response})
                    st.success("感谢您的反馈！")
            with col2:
                if st.button("👎 无用", key=f"useless_{len(st.session_state['message'])-1}"):
                    st.session_state["feedback"].append({"message_index": len(st.session_state['message'])-1, "feedback": "useless", "content": ai_response})
                    st.error("我们会继续改进！")