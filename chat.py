import os
import json
from openai import OpenAI

from search_api import SearchAPI
from parse_pages import PageParser
from section_filter import SectionFilter


class Chatter:
    def __init__(self, model_name = 'deepseek-r1:8b', reranker='../ckpts/bge-reranker-base'):
        self.model_name_all = ['deepseek-r1:8b']

        assert model_name in self.model_name_all
        self.model_name = model_name

        self.client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
        self.searcher = SearchAPI(agent_name='serper')
        self.parser = PageParser(parser_name='ra')
        self.section_filter = SectionFilter(reranker=reranker)

    def _get_prompt_with_rag(self, query, url_topk = 10, chunk_topk = 3):

        urls = self.searcher.search(query)
        urls = urls[:url_topk]

        raw_texts = self.parser.parse(urls)
        chunks = self.section_filter.get_chunked_text_batch(raw_texts, query, topk=chunk_topk)

        rag_info = ''
        for i, chunk in enumerate(chunks):
            rag_info += "{}\n###\n".format(chunk)

        prompt = '''请根据用户问题以及网上的搜索结果，给出高质量回答。

用户的问题是：{}

通过浏览器搜索的结果如下，包括多条搜索结果，以“###”分隔：

{}

请注意，网上的搜索结果仅供参考，不一定准确，也不一定和问题相关，请结合你的知识仔细辨别。
        '''.format(query, rag_info)

        return prompt





    def chat_no_rag(self, user_input, messages = None):
        if messages is None:
            messages = []
        messages.append({"role": "user", "content": user_input})

        r = self.client.chat.completions.create(model=self.model_name, messages=messages)
        reply = r.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        return reply, messages

    def chat_with_rag(self, user_input, messages = None):
        if messages is None:
            messages = []
        messages.append({"role": "user", "content": self._get_prompt_with_rag(user_input, url_topk=5, chunk_topk=3)})

        r = self.client.chat.completions.create(model=self.model_name, messages=messages)
        reply = r.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        return reply, messages
