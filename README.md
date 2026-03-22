使用时复制env.example文件内容，输入自己的api key
一个基于 `LangChain + FAISS + Qwen + Streamlit` 的本地 PDF 知识库问答系统。

## 功能说明

- 从 PDF 文档构建向量索引（FAISS）
- 通过相似度检索召回相关上下文
- 调用 Qwen 生成最终答案
- 提供 Streamlit Web 页面交互

## 项目结构

```text
rag_project/
|- app/
|  `- main.py                    # Streamlit 入口
|- config/
|  `- settings.py                # 环境变量与配置
|- loader/
|  `- pdf_loader.py              # PDF 加载逻辑
|- qwen/
|  `- qwen.py                    # Qwen 调用（含超时/重试）
|- rag/
|  `- rag_chain.py               # 检索与问答主链路
|- scripts/
|  |- build_index.py             # 索引构建入口（推荐）
|  |- build_index_core.py        # 索引构建核心逻辑
|  `- bulid_index.py             # 兼容旧脚本（已弃用）
|- vector_store/
|  `- faiss_store.py             # 向量库创建/安全读写
|- data/                         # PDF 数据目录
|- faiss_index/                  # 索引输出目录
`- requirements.txt
```

## 环境要求

- Python 3.9+
- DashScope 可用 API Key（用于 Qwen）
- 首次运行需可访问 Hugging Face（或配置镜像）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

1. 复制环境变量模板：

```bash
cp .env.example .env
```

Windows PowerShell 也可以用：

```powershell
Copy-Item .env.example .env
```

2. 修改 `.env`（至少配置 `DASHSCOPE_API_KEY`）：

```env
DASHSCOPE_API_KEY=your_dashscope_api_key_here
QWEN_MODEL=qwen-turbo
QWEN_REQUEST_TIMEOUT_SECONDS=60
QWEN_MAX_RETRIES=3
QWEN_RETRY_BACKOFF_SECONDS=1.0
HF_ENDPOINT=https://hf-mirror.com
# EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
# DATA_PATH=data/your_knowledge_file.pdf
```

参数说明：

- `DASHSCOPE_API_KEY`：必填
- `QWEN_MODEL`：Qwen 模型名，默认 `qwen-turbo`
- `QWEN_REQUEST_TIMEOUT_SECONDS`：单次请求超时（秒）
- `QWEN_MAX_RETRIES`：失败后最大重试次数
- `QWEN_RETRY_BACKOFF_SECONDS`：重试基础退避时间（秒，指数退避）
- `HF_ENDPOINT` / `HUGGINGFACE_ENDPOINT`：Hugging Face 镜像地址
- `EMBEDDING_MODEL`：Embedding 模型名或本地模型路径
- `DATA_PATH`：PDF 路径，默认 `data/knowledge.pdf`

## 准备数据

- 将 PDF 放入 `data/` 目录（推荐命名为 `knowledge.pdf`）
- 或在 `.env` 中设置 `DATA_PATH` 指向目标 PDF

## 构建索引

```bash
python scripts/build_index.py
```

构建成功后会在 `faiss_index/` 目录生成以下文件：

- `index.faiss`
- `docstore.json`
- `mapping.json`

## 启动应用

```bash
streamlit run app/main.py
```

打开页面后输入问题即可问答。

## 工作流程

1. `scripts/build_index.py` 读取 PDF 并构建向量索引
2. `vector_store/faiss_store.py` 以安全格式保存索引（FAISS 二进制 + JSON）
3. `rag/rag_chain.py` 执行 `similarity_search(k=3)` 召回上下文
4. `qwen/qwen.py` 调用 Qwen 生成回答（含超时、重试、退避）

## 已修复问题

- 移除对 `allow_dangerous_deserialization=True` 的依赖，避免危险反序列化
- Qwen 请求增加超时、重试与指数退避，提升网络抖动场景稳定性
- 新增 `scripts/build_index_core.py`，统一索引构建核心入口
- 保留 `scripts/bulid_index.py` 兼容旧命令，并标记为弃用

## 常见问题

- `Vector index not found`：
  - 先执行 `python scripts/build_index.py`
- `DASHSCOPE_API_KEY is empty`：
  - 检查 `.env` 或系统环境变量
- Embedding 模型加载失败：
  - 首次运行需联网，或配置 `HF_ENDPOINT`，或使用本地模型路径
- `PDF not found` / `PDF file is empty`：
  - 检查 `DATA_PATH` 是否正确

