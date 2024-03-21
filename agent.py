import time
from gpt_researcher.config import Config
from gpt_researcher.master.functions import *
from gpt_researcher.context.compression import ContextCompressor
from gpt_researcher.memory import Memory

class GPTResearcher:
    """
    GPT Researcher
    """
    def __init__(self, idea, report_type="idea_research_report", source_urls=None, config_path=None, websocket=None):
        """
        Initialize the GPT Researcher class.
        Args:
            idea:
            report_type:
            config_path:
            websocket:
        """
        self.idea = idea
        self.agent = None
        self.role = None
        self.report_type = report_type
        self.websocket = websocket
        self.cfg = Config(config_path)
        self.retriever = get_retriever(self.cfg.retriever)
        self.context = []
        self.source_urls = source_urls
        self.memory = Memory(self.cfg.embedding_provider)
        self.visited_urls = set()

    async def run(self):
        """
        Runs the GPT Researcher
        Returns:
            Report
        """
        print(f"🔎 Running research for '{self.idea}'...")
        # Generate Agent
        self.agent, self.role = await choose_agent(self.idea, self.cfg)
        await stream_output("logs", self.agent, self.websocket)

        # If specified, the researcher will use the given urls as the context for the research.
        if self.source_urls:
            self.context = await self.get_context_by_urls(self.source_urls)
        else:
            self.context = await self.get_context_by_idea(self.idea)

        # Write Research Report
        if self.report_type == "custom_report":
            self.role = self.cfg.agent_role if self.cfg.agent_role else self.role
        await stream_output("logs", f"✍️ Writing {self.report_type} for research task: {self.idea}...", self.websocket)
        report = await generate_report(idea=self.idea, context=self.context,
                                       agent_role_prompt=self.role, report_type=self.report_type,
                                       websocket=self.websocket, cfg=self.cfg)
        time.sleep(2)
        return report

    async def get_context_by_urls(self, urls):
        """
            Scrapes and compresses the context from the given urls
        """
        new_search_urls = await self.get_new_urls(urls)
        await stream_output("logs",
                            f"🧠 I will conduct my research based on the following urls: {new_search_urls}...",
                            self.websocket)
        scraped_sites = scrape_urls(new_search_urls, self.cfg)
        return await self.get_similar_content_by_idea(self.idea, scraped_sites)

    async def get_context_by_idea(self, idea):
        """
           Generates the context for the research task by searching the idea and scraping the results
        Returns:
            context: List of context
        """
        context = []
        # Generate Sub-Ideas including original idea
        sub_ideas = await get_sub_ideas(idea, self.role, self.cfg) + [idea]
        await stream_output("logs",
                            f"🧠 I will conduct my research based on the following ideas: {sub_ideas}...",
                            self.websocket)

        # Run Sub-Ideas
        for sub_idea in sub_ideas:
            await stream_output("logs", f"\n🔎 Running research for '{sub_idea}'...", self.websocket)
            scraped_sites = await self.scrape_sites_by_idea(sub_idea)
            content = await self.get_similar_content_by_idea(sub_idea, scraped_sites)
            await stream_output("logs", f"📃 {content}", self.websocket)
            context.append(content)

        return context

    async def get_new_urls(self, url_set_input):
        """ Gets the new urls from the given url set.
        Args: url_set_input (set[str]): The url set to get the new urls from
        Returns: list[str]: The new urls from the given url set
        """

        new_urls = []
        for url in url_set_input:
            if url not in self.visited_urls:
                await stream_output("logs", f"✅ Adding source url to research: {url}\n", self.websocket)

                self.visited_urls.add(url)
                new_urls.append(url)

        return new_urls

    async def scrape_sites_by_idea(self, sub_idea):
        """
        Runs a sub-idea
        Args:
            sub_idea:

        Returns:
            Summary
        """
        # Get Urls
        retriever = self.retriever(sub_idea)
        search_results = retriever.search(max_results=self.cfg.max_search_results_per_query)
        new_search_urls = await self.get_new_urls([url.get("href") for url in search_results])

        # Scrape Urls
        # await stream_output("logs", f"📝Scraping urls {new_search_urls}...\n", self.websocket)
        await stream_output("logs", f"🤔Researching for relevant information...\n", self.websocket)
        scraped_content_results = scrape_urls(new_search_urls, self.cfg)
        return scraped_content_results

    async def get_similar_content_by_idea(self, idea, pages):
        await stream_output("logs", f"📃 Getting relevant content based on idea: {idea}...", self.websocket)
        # Summarize Raw Data
        context_compressor = ContextCompressor(documents=pages, embeddings=self.memory.get_embeddings())
        # Run Tasks
        return context_compressor.get_context(idea, max_results=8)