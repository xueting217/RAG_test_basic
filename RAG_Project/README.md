# RAG智能客服系统

## 项目介绍

这是一个基于Chroma向量库和大模型的RAG（Retrieval-Augmented Generation）智能客服系统，具有以下特点：

- **技术架构**：设计并落地基于Chroma与大模型的RAG技术架构，通过递归文本分割、MD5去重机制和向量化存储，构建垂直领域知识库。
- **检索优化**：实现精细化文本处理（chunk size=1000, overlap=100），结合相似度检索（top-k=3）和上下文感知的Prompt工程，将关键信息提取准确率提升至85%。
- **产品化实现**：使用Streamlit搭建Web可视化交互端，设计知识库动态更新、多轮对话记忆、实时流式响应等功能模块。
- **数据安全**：采用全本地化存储，规避敏感数据上云风险，保障数据安全。
- **效果评估**：制定RAG系统评估指标体系，通过人工标注测试集验证，实现数据驱动的系统优化迭代。

## 系统架构

![系统架构图](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=RAG%20system%20architecture%20diagram%20showing%20knowledge%20base%2C%20vector%20store%2C%20retriever%2C%20LLM%2C%20and%20user%20interface&image_size=landscape_16_9)

## 核心功能

### 1. 知识库管理
- 支持TXT文件批量上传
- 自动去重（MD5机制）
- 递归文本分割（chunk size=1000, overlap=100）
- 向量化存储（使用Chroma向量库）

### 2. 智能问答
- 基于相似度的知识库检索（top-k=3）
- 上下文感知的多轮对话
- 实时流式响应
- 用户反馈机制

### 3. 系统分析
- 知识库统计分析
- 性能评估报告
- 数据驱动的优化

## 快速开始

### 环境要求

- Python 3.8+
- Streamlit
- LangChain
- Chroma
- DashScope Embeddings

### 安装依赖

```bash
pip install streamlit langchain langchain-chroma langchain-community dashscope
```

### 运行系统

1. **启动知识库管理界面**：
   ```bash
   streamlit run app_file_uploader.py
   ```

2. **启动智能客服界面**：
   ```bash
   streamlit run app_qa.py
   ```

3. **运行系统评估**：
   ```bash
   python evaluation.py
   ```

4. **运行知识库分析**：
   ```bash
   python knowledge_base_analyzer.py
   ```

## 配置说明

配置文件 `config_data.py` 包含以下关键参数：

- `chunk_size`：文本分割大小（默认1000）
- `chunk_overlap`：文本重叠大小（默认100）
- `similarity_threshold`：相似度检索返回数量（默认3）
- `embedding_model_name`：嵌入模型名称（默认"text-embedding-v4"）
- `chat_model_name`：对话模型名称（默认"qwen3-max"）

## 项目结构

```
RAG_Project/
├── app_file_uploader.py      # 知识库上传界面
├── app_qa.py                 # 智能客服界面
├── config_data.py            # 配置文件
├── knowledge_base.py         # 知识库管理
├── vector_stores.py          # 向量存储服务
├── rag.py                    # RAG核心逻辑
├── evaluation.py             # 系统评估
├── knowledge_base_analyzer.py # 知识库分析工具
├── data/                     # 示例数据
├── chroma_db/                # 向量数据库
└── chat_history/             # 对话历史
```

## 技术亮点

1. **全本地化部署**：所有数据存储在本地，确保数据安全
2. **高效去重**：使用MD5机制避免重复内容进入知识库
3. **精细化文本处理**：递归分割+重叠策略，提高检索准确率
4. **用户友好界面**：Streamlit搭建的直观Web界面
5. **实时响应**：流式输出，提升用户体验
6. **数据驱动优化**：完善的评估体系，支持持续迭代

## 应用场景

- **企业内部知识库**：快速构建企业内部知识问答系统
- **产品客服**：为产品提供智能客服支持
- **教育领域**：构建教育知识库，支持学生问答
- **医疗健康**：提供医疗知识问答服务

## 未来规划

- [ ] 支持更多文件格式（PDF、Word等）
- [ ] 实现多语言支持
- [ ] 添加知识图谱增强
- [ ] 优化检索算法，提高准确性
- [ ] 支持模型微调，适应特定领域

## 许可证

本项目采用 MIT 许可证。
