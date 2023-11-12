from gpt_researcher.agents.gpt_researcher.functions import *


class GPTResearcher:
    def __init__(self, query, report_type, websocket=None):
        self.query = query
        self.agent = None
        self.role = None
        self.report_type = report_type
        self.websocket = websocket
        self.retriever = get_retriever()
        self.context = []

    async def run(self):
        # Generate Agent
        self.agent, self.role = choose_agent(self.query)
        await self.stream_output(self.agent)

        # Generate Sub-Queries
        sub_queries = get_sub_queries(self.query, self.role)
        await self.stream_output(sub_queries)

        # Run Sub-Queries
        for sub_query in sub_queries:
            await self.stream_output(sub_query)
            context = self.run_sub_query(sub_query)
            self.context.append(context)
            await self.stream_output(context)

        # Conduct Research
        report = generate_report(query=self.query, context=self.context,
                                       agent_role_prompt=self.role, report_type=self.report_type)
        await self.stream_output(report)

        return report

    def run_sub_query(self, sub_query):
        # Get Urls
        retriever = self.retriever(sub_query)
        urls = retriever.search()

        # Scrape Urls
        raw_data = scrape_urls(urls)

        # Summarize Raw Data
        summary = summarize(query=sub_query, text=raw_data, agent_role_prompt=self.role)

        # Run Tasks
        return summary

    async def stream_output(self, output):
        if not self.websocket:
            return print(output)
        await self.websocket.send_json({"type": "logs", "output": output})

