## 各环节支持配置
- LLM
    - DeepSeek-R1 8B
- 搜索API
    - serper
- 网页解析
    - readability
- 文本切分
    - langchain_text_splitters.RecursiveCharacterTextSplitter
- 文本相关性排序
    - bge-reranker-base


## 部署DeepSeek-R1 8B

```shell
brew install ollama # mac
curl -fsSL https://ollama.com/install.sh | sh # linux

ollama serve # 打开服务才能通过openai接口调用

ollama run deepseek-r1:8b # 自动下载模型，下载完成后kill掉
```

## 下载文本切分模型

[BAAI/bge-reranker-base](https://hf-mirror.com/BAAI/bge-reranker-base)


## 有RAG结果

[result_with_rag.md](./result_with_rag.md)

## 无RAG结果

[result_no_rag.md](./result_no_rag.md)