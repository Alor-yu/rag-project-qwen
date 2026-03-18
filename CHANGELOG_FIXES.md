# 项目错误与修复修改日志

> 生成时间：2026-03-18  
> 说明：当前目录无 `.git` 历史，以下内容基于现有源码可追溯信息与本次运行验证结果整理。

## 一、代码中已体现的错误处理与修复

### 1. 索引脚本入口命名问题（`bulid` 拼写）
- 错误现象：历史脚本名为 `scripts/bulid_index.py`（`build` 拼写错误），易导致执行命令不统一。
- 解决办法：新增 `scripts/build_index.py` 作为标准入口，并转调 `scripts.bulid_index.main`，统一推荐命令为：
  - `python scripts/build_index.py`
- 相关文件：`scripts/build_index.py`、`scripts/bulid_index.py`

### 2. PDF 文件路径/空文件导致构建失败
- 错误现象：索引构建时，若 PDF 不存在或为空，会在加载阶段失败。
- 解决办法：在加载层增加前置校验并给出明确异常：
  - 不存在：`FileNotFoundError("PDF not found: ...")`
  - 空文件：`ValueError("PDF file is empty: ...")`
- 相关文件：`loader/pdf_loader.py`

### 3. 默认知识库文件名不匹配导致找不到数据
- 错误现象：默认路径为 `data/knowledge.pdf`，若实际文件名不同会导致加载失败。
- 解决办法：配置层增加候选回退逻辑：当默认文件不存在且 `data/` 下仅有一个 PDF 时自动选用该文件。
- 相关文件：`config/settings.py`

### 4. 向量索引不存在时查询直接失败
- 错误现象：未先构建 FAISS 索引就提问会报错。
- 解决办法：查询前检查索引目录，不存在时抛出明确异常并提示执行构建命令。
- 相关文件：`rag/rag_chain.py`

### 5. Embedding 模型首次下载/加载失败
- 错误现象：首次运行需要下载 HuggingFace 模型，网络受限时会失败。
- 解决办法：在索引构建与查询阶段统一捕获并抛出可操作错误，提示三种处理路径：
  - 保证首次联网
  - 配置 `HF_ENDPOINT` / `HUGGINGFACE_ENDPOINT`
  - `EMBEDDING_MODEL` 指向本地模型目录
- 相关文件：`vector_store/faiss_store.py`、`rag/rag_chain.py`

### 6. Qwen 接口调用失败/空返回
- 错误现象：可能出现 API Key 为空、接口返回非 200、返回文本为空。
- 解决办法：增加分支校验并抛出明确异常，避免静默失败。
- 相关文件：`qwen/qwen.py`

### 7. 前端报错信息可读性
- 错误现象：Streamlit 页面异常时用户难以判断下一步。
- 解决办法：页面层增加针对性异常提示：
  - 索引缺失提示执行构建
  - 其他异常展示具体错误文本
- 相关文件：`app/main.py`

## 二、本次验证新发现问题（待修复）

### 1. `get_dashscope_api_key` 缺失导致导入失败（阻塞）
- 错误现象：`qwen/qwen.py` 从 `config.settings` 导入 `get_dashscope_api_key`，但 `settings.py` 中不存在该函数。
- 可复现命令：
  - `venv\Scripts\python.exe -c "import qwen.qwen"`
- 实际报错：
  - `ImportError: cannot import name 'get_dashscope_api_key' from 'config.settings'`
- 影响范围：`qwen.qwen`、`rag.rag_chain` 导入链路均会失败。
- 建议修复：
  - 在 `config/settings.py` 增加 `get_dashscope_api_key()`
  - 如需支持 `.env`，同时增加 `load_dotenv()` 初始化

### 2. 网络受限导致 Embedding 模型下载失败
- 错误现象：构建索引时访问 HuggingFace 被系统/网络策略拦截。
- 可复现命令：
  - `venv\Scripts\python.exe scripts/build_index.py`
- 实际报错关键字：
  - `[WinError 10013] ... 访问套接字的尝试被拒绝`
  - `Build index failed: Failed to load embedding model...`
- 建议修复：
  - 配置可用镜像：`HF_ENDPOINT` 或 `HUGGINGFACE_ENDPOINT`
  - 或将 `EMBEDDING_MODEL` 改为本地模型路径

## 三、后续维护建议

- 每次修复错误后，按“错误现象 / 根因 / 解决办法 / 影响范围 / 回归验证命令”追加到本文件。
- 建议补齐 `git` 仓库历史，以便后续基于提交记录自动生成更完整的变更日志。
