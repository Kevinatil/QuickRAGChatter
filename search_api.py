import os
import json
import requests

from warnings import warn


class SearchAPI:
    def __init__(self, agent_name = 'serper'):
        self.agent_names_all = ['serper']

        assert agent_name in self.agent_names_all

        self.agent_name = agent_name

        self.api_key = self._get_api_key()

    def _get_api_key(self):
        with open('config.json', 'r') as f:
            key = json.load(f)['API_KEY']['serper']
        return key

    def _search_serper(self, query):
        headers = {
        'X-API-KEY': self.api_key,
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", "https://google.serper.dev/search", headers=headers, data=json.dumps({"q": query}))
        urls = json.loads(response.text)['organic']
        urls = [url['link'] for url in urls]
        return urls
    
    def _judge_available(self, agent_name):
        return True

    def search(self, query):
        func = None
        if self._judge_available(self.agent_name):
            func = getattr(self, '_search_{}'.format(self.agent_name))
        else:
            warn('{} not available, trying other agents'.format(self.agent_name), Warning)
            for name in self.agent_names_all:
                if name != self.agent_name and self._judge_available(name):
                    func = getattr(self, '_search_{}'.format(name))
        if func is None:
            warn('All search agents are not available.', Warning)
            return []
        
        urls = func(query)

        if len(urls) == 0:
            warn('No urls available.')

        return urls



if __name__ == "__main__":
    searcher = SearchAPI('serper')

    searcher.search('半导体现状')