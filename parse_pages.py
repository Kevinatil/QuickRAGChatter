from readability import Document
import requests, concurrent.futures
import html2text

from warnings import warn

class PageParser:
    def __init__(self, parser_name = 'ra'):
        self.parser_name_all = ['ra']

        assert parser_name in self.parser_name_all
        self.parser_name = parser_name

        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = True

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

    def _judge_usable(self, text):
        if len(text) < 50:
            return False
        return True

    def _parse_ra(self, url):
        try:
            r = requests.get(url, headers=self.headers)
            r.encoding = r.apparent_encoding
            doc = Document(r.text)
            doc = self.h2t.handle(doc.summary()).strip()
            if self._judge_usable(doc):
                return doc
            else:
                return ""
        except Exception as e:
            warn('{} err'.format(url), Warning)
            print(e)
        
        return ""

    def parse(self, urls):
        if type(urls) == 'str':
            urls = [urls]
        
        with concurrent.futures.ThreadPoolExecutor(10) as exe:
            texts = list(exe.map(getattr(self, '_parse_{}'.format(self.parser_name)), urls))
        texts = [text for text in texts if len(text) > 0]

        return texts



if __name__ == "__main__":
    parser = PageParser(parser_name='ra')

    urls = ['https://www.semi.org.cn/site/semi/article/cc457d5c949d407da0940aabd4f8066c.html', 
            'https://pdf.dfcfw.com/pdf/H3_AP202509161744585471_1.pdf?1758011945000.pdf', 
            'https://zhuanlan.zhihu.com/p/1936540183647490937', 
            'https://finance.sina.com.cn/cj/2024-12-03/doc-incyctzu4757692.shtml', 
            'https://www.voachinese.com/a/world-media-on-china---new-heroic-effort-to-boost-semiconductor-industry-20240529/7633345.html']

    ret = parser.parse(urls)

    for i, text in enumerate(ret):
        with open('{}.txt'.format(i), 'w') as f:
            f.write(text)