# Description: Research assistant class that handles the research process for a given question.

# libraries
import asyncio
import json
import hashlib

from gpt_researcher.actions.web_search import web_search
from gpt_researcher.actions.web_scrape import async_browse
from gpt_researcher.retriever.llm_utils import choose_agent
from gpt_researcher.processing.text import \
    write_to_file, \
    create_message, \
    create_chat_completion, \
    read_txt_files, \
    write_md_to_pdf
from config import Config
from gpt_researcher.retriever import prompts
import os


class RetrieverAgent:
    def __init__(self, question, researcher, websocket=None):
        self.question = question
        self.researcher = researcher
        self.websocket = websocket
        self.agent_role_prompt = choose_agent(
            self.researcher.smart_llm_model,
            self.researcher.llm_provider,
            question
        ).get("agent_role_prompt") or "Assist me with this research topic"
        self.research_summary = ""
        self.visited_urls = set()
        self.dir_path = f"../outputs/{hashlib.sha1(question.encode()).hexdigest()}"

    async def prepare_directories(self):
        os.makedirs(self.dir_path, exist_ok=True)

    async def stream_output(self, output):
        if not self.websocket:
            return print(output)
        await self.websocket.send_json({"type": "logs", "output": output})

    async def summarize(self, text, topic):
        """ Summarizes the given text for the given topic.
        Args: text (str): The text to summarize
                topic (str): The topic to summarize the text for
        Returns: str: The summarized text
        """

        messages = [create_message(text, topic)]
        await self.stream_output(f"📝 Summarizing text for query: {text}")

        return create_chat_completion(
            model=self.researcher.fast_llm_model,
            temperature=self.researcher.temperature,
            messages=messages,
        )

    async def get_new_urls(self, url_set_input):
        """ Gets the new urls from the given url set.
        Args: url_set_input (set[str]): The url set to get the new urls from
        Returns: list[str]: The new urls from the given url set
        """

        new_urls = []
        for url in url_set_input:
            if url not in self.visited_urls:
                await self.stream_output(f"✅ Adding source url to research: {url}\n")

                self.visited_urls.add(url)
                new_urls.append(url)

        return new_urls

    async def call_agent(self, action, stream=False, websocket=None):
        messages = [{
            "role": "system",
            "content": self.agent_role_prompt
        }, {
            "role": "user",
            "content": action,
        }]
        answer = create_chat_completion(
            model=self.researcher.smart_llm_model,
            messages=messages,
            stream=stream,
            websocket=websocket,
            llm_provider=self.researcher.llm_provider
        )
        return answer

    async def create_search_queries(self):
        """ Creates the search queries for the given question.
        Args: None
        Returns: list[str]: The search queries for the given question
        """
        result = await self.call_agent(prompts.generate_search_queries_prompt(self.question))
        await self.stream_output(f"🧠 I will conduct my research based on the following queries: {result}...")
        return json.loads(result)

    async def async_search(self, query):
        """ Runs the async search for the given query.
        Args: query (str): The query to run the async search for
        Returns: list[str]: The async search for the given query
        """
        search_results = json.loads(web_search(self.researcher.search_api, query))
        new_search_urls = self.get_new_urls([url.get("href") for url in search_results])

        await self.stream_output(f"🌐 Browsing the following sites for relevant information: {new_search_urls}...")

        # Create a list to hold the coroutine objects
        tasks = [async_browse(
            self.researcher.selenium_web_browser,
            self.researcher.user_agent,
            self.researcher.fast_llm_model,
            self.researcher.summary_token_limit,
            self.researcher.llm_provider,
            url,
            query,
            self.websocket
        )
            for url in await new_search_urls]

        # Gather the results as they become available
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        return responses

    async def run_search_summary(self, query):
        """ Runs the search summary for the given query.
        Args: query (str): The query to run the search summary for
        Returns: str: The search summary for the given query
        """

        await self.stream_output(f"🔎 Running research for '{query}'...")

        responses = await self.async_search(query)

        result = "\n".join(responses)
        os.makedirs(os.path.dirname(f"{self.dir_path}/research-{query}.txt"), exist_ok=True)
        write_to_file(f"{self.dir_path}/research-{query}.txt", result)
        return result

    async def conduct_research(self):
        """ Conducts the research for the given question.
        Args: None
        Returns: str: The research for the given question
        """
        self.research_summary = read_txt_files(self.dir_path) if os.path.isdir(self.dir_path) else ""

        if not self.research_summary:
            search_queries = await self.create_search_queries()
            for query in search_queries:
                research_result = await self.run_search_summary(query)
                self.research_summary += f"{research_result}\n\n"

        await self.stream_output(f"Total research words: {len(self.research_summary.split(' '))}")

        return self.research_summary

    async def create_concepts(self):
        """ Creates the concepts for the given question.
        Args: None
        Returns: list[str]: The concepts for the given question
        """
        result = self.call_agent(prompts.generate_concepts_prompt(self.question, self.research_summary))

        await self.stream_output(f"I will research based on the following concepts: {result}\n")
        return json.loads(result)

    async def write_report(self, report_type, websocket=None):
        """ Writes the report for the given question.
        Args: None
        Returns: str: The report for the given question
        """
        report_type_func = prompts.get_report_by_type(report_type)
        await self.stream_output(f"✍️ Writing {report_type} for research task: {self.question}...")

        answer = await self.call_agent(report_type_func(self.question, self.research_summary),
                                       stream=websocket is not None, websocket=websocket)
        # if websocket is True than we are streaming gpt response, so we need to wait for the final response
        final_report = await answer if websocket else answer

        path = await write_md_to_pdf(report_type, self.dir_path, final_report)

        return answer, path

    async def write_lessons(self):
        """ Writes lessons on essential concepts of the research.
        Args: None
        Returns: None
        """
        concepts = await self.create_concepts()
        for concept in concepts:
            answer = await self.call_agent(prompts.generate_lesson_prompt(concept), stream=True)
            await write_md_to_pdf("Lesson", self.dir_path, answer)
