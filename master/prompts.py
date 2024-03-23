from datetime import datetime


def generate_search_queries_prompt(question, max_iterations=3):
    """ Generates the search queries prompt for the given question.
    Args: question (str): The question to generate the search queries prompt for
    Returns: str: The search queries prompt for the given question
    """

    return f'Write {max_iterations} google search queries to search online that form an objective opinion from the following: "{question}"' \
           f'Use the current date if needed: {datetime.now().strftime("%B %d, %Y")}.\n' \
           f'You must respond with a list of strings in the following format: ["query 1", "query 2", "query 3"].'


def generate_report_prompt(question, context, report_format="apa", total_words=1000):
    """ Generates the report prompt for the given question and research summary.
    Args: question (str): The question to generate the report prompt for
            research_summary (str): The research summary to generate the report prompt for
    Returns: str: The report prompt for the given question and research summary
    """

    return f'Information: """{context}"""\n\n' \
           f'Using the above information, answer the following' \
           f' query or task: "{question}" in a detailed report --' \
           " The report should focus on the answer to the query, should be well structured, informative," \
           f" in depth and comprehensive, with facts and numbers if available and a minimum of {total_words} words.\n" \
           "You should strive to write the report as long as you can using all relevant and necessary information provided.\n" \
           "You must write the report with markdown syntax.\n " \
           f"Use an unbiased and journalistic tone. \n" \
           "You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.\n" \
           f"You MUST write all used source urls at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each.\n" \
           f"You MUST write the report in {report_format} format.\n " \
            f"Cite search results using inline notations. Only cite the most \
            relevant results that answer the query accurately. Place these citations at the end \
            of the sentence or paragraph that reference them.\n"\
            f"Please do your best, this is very important to my career. " \
            f"Assume that the current date is {datetime.now().strftime('%B %d, %Y')}"


def generate_resource_report_prompt(question, context, report_format="apa", total_words=1000):
    """Generates the resource report prompt for the given question and research summary.

    Args:
        question (str): The question to generate the resource report prompt for.
        context (str): The research summary to generate the resource report prompt for.

    Returns:
        str: The resource report prompt for the given question and research summary.
    """
    return f'"""{context}"""\n\nBased on the above information, generate a bibliography recommendation report for the following' \
           f' question or topic: "{question}". The report should provide a detailed analysis of each recommended resource,' \
           ' explaining how each source can contribute to finding answers to the research question.\n' \
           'Focus on the relevance, reliability, and significance of each source.\n' \
           'Ensure that the report is well-structured, informative, in-depth, and follows Markdown syntax.\n' \
           'Include relevant facts, figures, and numbers whenever available.\n' \
           'The report should have a minimum length of 700 words.\n' \
            'You MUST include all relevant source urls.'

def generate_custom_report_prompt(query_prompt, context, report_format="apa", total_words=1000):
    return f'"{context}"\n\n{query_prompt}'


def generate_outline_report_prompt(question, context, report_format="apa", total_words=1000):
    """ Generates the outline report prompt for the given question and research summary.
    Args: question (str): The question to generate the outline report prompt for
            research_summary (str): The research summary to generate the outline report prompt for
    Returns: str: The outline report prompt for the given question and research summary
    """

    return f'"""{context}""" Using the above information, generate an outline for a research report in Markdown syntax' \
           f' for the following question or topic: "{question}". The outline should provide a well-structured framework' \
           ' for the research report, including the main sections, subsections, and key points to be covered.' \
           ' The research report should be detailed, informative, in-depth, and a minimum of 1,200 words.' \
           ' Use appropriate Markdown syntax to format the outline and ensure readability.'


def get_report_by_type(report_type):
    report_type_mapping = {
        'research_report': generate_report_prompt,
        'resource_report': generate_resource_report_prompt,
        'outline_report': generate_outline_report_prompt,
        'custom_report': generate_custom_report_prompt
    }
    return report_type_mapping[report_type]


def auto_agent_instructions():
    return """
        This task is centered on conducting in-depth research into existing ideas, analyzing their feasibility, impact, and potential for further development. It utilizes a dedicated server designed for the exploration and examination of creative concepts, with each server employing tailored approaches to assess and enrich the original ideas provided. The research is conducted by a specific server, defined by its type and role, with each server requiring distinct instructions.

        Agent

        The server is determined by the field of the topic and the specific name of the server that could be utilized to research the topic provided. Agents are categorized by their area of expertise, and each server type is associated with a corresponding emoji. Respond with a JSON object.

        examples:
        task: "What is the current trend in electric vehicle battery technologies?"
        response: 
        {
            "server": "🔋 Market Intelligence Agent",
            "agent_role_prompt": "As an AI researcher specializing in the electric vehicle (EV) battery market, your task is to systematically scour through global market reports, industry publications, and recent news articles. You are expected to identify and analyze key trends in EV battery technology, including advancements in battery efficiency, cost reduction efforts, and emerging players in the market. Compile your findings into a comprehensive report that outlines current trends, projects future developments, and highlights the technologies with the most disruptive potential. The output should be a detailed summary including market size, predicted growth, and key technological innovations."
        }

        task: "Who are the leading competitors in the plant-based meat industry?"
        response: 
        {
            "server": "🌱 Competitor Intelligence Agent",
            "agent_role_prompt": "You are an AI-driven competitive analyst for the plant-based meat industry. Begin by identifying the major and emerging companies in this sector. Use business directories, financial reports, and industry news to gather data on these competitors. Analyze their market share, product offerings, distribution channels, and recent strategic moves. Your goal is to compile a competitive landscape report that provides insights into the strengths and weaknesses of these competitors, identifies market trends, and offers an overview of the competitive dynamics in the plant-based meat industry. The output should be a structured report with profiles on each competitor and an analysis of market trends."
        }

        task: "How are AI technologies being integrated into home appliances?"
        response: 
        {
            "server": "📈 Trend Analysis Agent",
            "agent_role_prompt": "As an AI expert in technology trends, your mission is to investigate the integration of AI into home appliances. Dive into consumer electronics reports, product release announcements, and technology forums to collect information on AI-enabled home appliances. Focus on identifying the types of appliances that are being enhanced with AI, the functionalities being introduced, and the consumer response to these innovations. Synthesize this information into a trend analysis report that covers the current state of AI in home appliances, predicts future innovations, and assesses the potential impact on consumer behavior. The output should include examples of AI applications in home appliances and forecasted trends."
        }

        task: "What are the main concerns of consumers regarding smart home devices?"
        response: 
        {
            "server": "👥 Customer Insights Agent",
            "agent_role_prompt": "Your role is to understand the consumer perspective on smart home devices. Through an analysis of online customer reviews, social media conversations, forum discussions, and consumer surveys, gather data on consumer concerns, preferences, and usage patterns related to smart home technologies. Analyze this data to identify common themes and insights into what consumers value most and what reservations they have. Compile your findings into a detailed insights report that includes consumer pain points, desired features, and expectations from smart home devices. The output should offer actionable insights for companies looking to improve or develop new smart home technologies."
        }

        task: "Identify potential technological breakthroughs in renewable energy storage."
        response: 
        {
            "server": "💡 Innovation Scouting Agent",
            "agent_role_prompt": "You are tasked with scouting emerging technologies in the renewable energy storage sector. Explore academic journals, patent databases, tech incubator reports, and industry conference proceedings to identify groundbreaking technologies and research in energy storage. Evaluate these technologies for their innovation, potential impact, scalability, and the challenges they aim to solve. Your objective is to compile an innovation scouting report that highlights the most promising technologies, assesses their market readiness, and predicts their potential to disrupt the renewable energy storage market. The output should be a curated list of breakthrough technologies with an analysis of their implications for the industry."
        }

        task: "What resources are required to manufacture an electric vehicle, and what are the cost implications?"
        response: 
        {
            "server": "🛠 Resource Analysis Agent",
            "agent_role_prompt": "As an AI analyst focused on resource analysis for electric vehicle production, your mission is to investigate the materials, components, and technologies needed for manufacturing electric vehicles. Explore industry supply chains, raw material costs, labor market trends, and technological advancements in manufacturing processes. Your task is to provide a detailed analysis of the resources required, including the availability and cost implications of these resources. Assess potential bottlenecks in the supply chain and recommend strategies for cost optimization. The output should include a comprehensive breakdown of manufacturing costs, resource availability, and strategic recommendations for efficient production."
        }
    """

def generate_summary_prompt(query, data):
    """ Generates the summary prompt for the given question and text.
    Args: question (str): The question to generate the summary prompt for
            text (str): The text to generate the summary prompt for
    Returns: str: The summary prompt for the given question and text
    """

    return f'{data}\n Using the above text, summarize it based on the following task or query: "{query}".\n If the ' \
           f'query cannot be answered using the text, YOU MUST summarize the text in short.\n Include all factual ' \
           f'information such as numbers, stats, quotes, etc if available. '

