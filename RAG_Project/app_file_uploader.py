"""
基于Streamlit完成WEB网页上传服务

pip install streamlit

Streamlit：当WEB页面元素发生变化，则代码重新执行一遍
"""
import time
import os

import streamlit as st
from knowledge_base import KnowledgeBaseService
# 添加网页标题
st.title("知识库更新服务")

# 添加自定义样式
st.markdown("""
<style>
.file-card {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.success-message {
    color: #155724;
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    padding: 10px;
    border-radius: 5px;
    margin-top: 10px;
}
.error-message {
    color: #721c24;
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    padding: 10px;
    border-radius: 5px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# file_uploader - 支持批量上传
uploader_files = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=True,    # True表示支持批量上传
    help="支持同时上传多个TXT文件到知识库"
)

# session_state就是一个字典
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if "upload_history" not in st.session_state:
    st.session_state["upload_history"] = []

# 显示上传历史
if st.session_state["upload_history"]:
    with st.expander("上传历史"):
        for item in st.session_state["upload_history"]:
            st.markdown(f"**{item['file_name']}** - {item['status']} - {item['time']}")

# 批量处理上传的文件
if uploader_files:
    st.subheader("上传文件列表")
    
    # 显示文件信息
    for i, uploader_file in enumerate(uploader_files):
        file_name = uploader_file.name
        file_type = uploader_file.type
        file_size = uploader_file.size / 1024    # KB
        
        with st.container():
            st.markdown(f'<div class="file-card">', unsafe_allow_html=True)
            st.subheader(f"文件 {i+1}: {file_name}")
            st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")
            
            # 显示文件内容预览
            text = uploader_file.getvalue().decode("utf-8")
            with st.expander("预览内容"):
                st.text_area("文件内容", text, height=150, disabled=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 批量导入按钮
    if st.button("批量导入知识库"):
        total_files = len(uploader_files)
        success_count = 0
        error_count = 0
        
        with st.spinner("正在批量导入知识库..."):
            for uploader_file in uploader_files:
                try:
                    file_name = uploader_file.name
                    text = uploader_file.getvalue().decode("utf-8")
                    result = st.session_state["service"].upload_by_str(text, file_name)
                    
                    # 记录上传历史
                    st.session_state["upload_history"].append({
                        "file_name": file_name,
                        "status": "成功" if "成功" in result else "失败",
                        "time": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    if "成功" in result:
                        success_count += 1
                        st.markdown(f'<div class="success-message">{file_name} - {result}</div>', unsafe_allow_html=True)
                    else:
                        error_count += 1
                        st.markdown(f'<div class="error-message">{file_name} - {result}</div>', unsafe_allow_html=True)
                    
                    time.sleep(0.5)  # 避免请求过快
                except Exception as e:
                    error_count += 1
                    st.markdown(f'<div class="error-message">{file_name} - 导入失败: {str(e)}</div>', unsafe_allow_html=True)
                    st.session_state["upload_history"].append({
                        "file_name": file_name,
                        "status": f"失败: {str(e)}",
                        "time": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
        
        # 显示导入结果
        st.success(f"批量导入完成！成功: {success_count}, 失败: {error_count}, 总计: {total_files}")




