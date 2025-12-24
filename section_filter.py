from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import CrossEncoder


class SectionFilter:
    def __init__(self, reranker, chunk_size = 300, chunk_overlap = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "。", ". ", "！", "？"]
        )
        self.reranker = reranker
    
    def get_chunked_text(self, text, query, topk: int = None):
        chunks = self.splitter.split_text(text)

        reranker = CrossEncoder(self.reranker)
        scores = reranker.predict([(query, text) for text in chunks])
        ranked = sorted(zip(scores, chunks), reverse=True)
        chunks = [txt for _, txt in ranked]
        if topk is None:
            return chunks
        else:
            return chunks[:topk]

    def get_chunked_text_batch(self, texts, query, topk: int = None):
        ret = []

        for text in texts:
            ret.extend(self.get_chunked_text(text, query, topk))
        
        return ret