from itertools import islice
from duckduckgo_search import DDGS


class Duckduckgo:
    """
    Duckduckgo API Retriever
    """
    def __init__(self):
        self.ddg = DDGS()

    def search(self, query, max_results=5):
        """
        Performs the search
        :param query:
        :param max_results:
        :return:
        """
        ddgs_gen = self.ddg.text(query, region='wt-wt')
        urls = [r["href"] for r in islice(ddgs_gen, max_results)]
        return urls