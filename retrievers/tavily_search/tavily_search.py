# Tavily API Retriever

# libraries
import os
from tavily import TavilyClient
from duckduckgo_search import DDGS


class TavilySearch():
    """
    Tavily API Retriever
    """
    def __init__(self, idea):
        """
        Initializes the TavilySearch object
        Args:
            idea:
        """
        self.idea = idea
        self.api_key = self.get_api_key()
        self.client = TavilyClient(self.api_key)

    def get_api_key(self):
        """
        Gets the Tavily API key
        Returns:

        """
        # Get the API key
        try:
            api_key = os.environ["TAVILY_API_KEY"]
        except:
            raise Exception("Tavily API key not found. Please set the TAVILY_API_KEY environment variable. "
                            "You can get a key at https://app.tavily.com")
        return api_key

    def research(self, max_results=7):
        """
        Researches the idea
        Returns:

        """
        try:
            # Generate queries for researching the idea
            queries = [self.idea + ' market research', self.idea + ' competitors', self.idea + ' demand', self.idea + ' features', self.idea + ' viability', self.idea + ' resources', self.idea + ' tech stack']
            # Search the queries
            results = [self.client.search(query, search_depth="advanced", max_results=max_results) for query in queries]
            # Return the results
            research_response = [{"query": query, "results": [{"href": obj["url"], "body": obj["content"]} for obj in result.get("results", [])]} for query, result in zip(queries, results)]
        except Exception as e: # Fallback in case overload on Tavily Search API
            ddg = DDGS()
            research_response = [{"query": query, "results": ddg.text(query, region='wt-wt', max_results=max_results)} for query in queries]
        return research_response