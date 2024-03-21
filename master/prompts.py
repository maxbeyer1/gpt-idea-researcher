from datetime import datetime


def generate_idea_research_queries_prompt(idea, max_iterations=3):
    """ Generates the idea research queries prompt for the given idea.
    Args: idea (str): The idea to generate the idea research queries prompt for
    Returns: str: The idea research queries prompt for the given idea
    """

    return f'Write {max_iterations} google search queries to research the following idea: "{idea}"' \
           f'Include queries for market research, competitors, demand, features, viability, resources, tech stack, etc.' \
           f'Use the current date if needed: {datetime.now().strftime("%B %d, %Y")}.' \
           f'You must respond with a list of strings in the following format: ["query 1", "query 2", "query 3"].'


def generate_idea_research_report_prompt(idea, context, report_format="apa", total_words=1000):
    """ Generates the idea research report prompt for the given idea and research summary.
    Args: idea (str): The idea to generate the idea research report prompt for
            research_summary (str): The research summary to generate the idea research report prompt for
    Returns: str: The idea research report prompt for the given idea and research summary
    """

    return f'Information: """{context}"""' \
           f'Using the above information, research the following' \
           f' idea: "{idea}" in a detailed report --' \
           " The report should focus on the idea, including market research, competitors, demand, features, viability, resources, tech stack, etc. It should be well structured, informative," \
           f" in depth and comprehensive, with facts and numbers if available and a minimum of {total_words} words." \
           "You should strive to write the report as long as you can using all relevant and necessary information provided." \
           "You must write the report with markdown syntax." \
           f"Use an unbiased and journalistic tone." \
           "You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions." \
           f"You MUST write all used source urls at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each." \
           f"You MUST write the report in {report_format} format." \
            f"Cite search results using inline notations. Only cite the most " \
            f"relevant results that answer the query accurately. Place these citations at the end " \
            f"of the sentence or paragraph that reference them."\
            f"Please do your best, this is very important to my career. " \
            f"Assume that the current date is {datetime.now().strftime('%B %d, %Y')}"


def get_report_by_type(report_type):
    report_type_mapping = {
        'research_report': generate_report_prompt,
        'resource_report': generate_resource_report_prompt,
        'outline_report': generate_outline_report_prompt,
        'custom_report': generate_custom_report_prompt,
        'idea_research_report': generate_idea_research_report_prompt
    }
    return report_type_mapping[report_type]


def auto_agent_instructions():
    return """
        This task involves researching a given topic, regardless of its complexity or the availability of a definitive answer. The research is conducted by a specific server, defined by its type and role, with each server requiring distinct instructions.
        Agent
        The server is determined by the field of the topic and the specific name of the server that could be utilized to research the topic provided. Agents are categorized by their area of expertise, and each server type is associated with a corresponding emoji.

        examples:
        task: "should I invest in apple stocks?"
        response: 
        {
            "server": "💰 Finance Agent",
            "agent_role_prompt: "You are a seasoned finance analyst AI assistant. Your primary goal is to compose comprehensive, astute, impartial, and methodically arranged financial reports based on provided data and trends."
        }
        task: "could reselling sneakers become profitable?"
        response: 
        { 
            "server":  "📈 Business Analyst Agent",
            "agent_role_prompt": "You are an experienced AI business analyst assistant. Your main objective is to produce comprehensive, insightful, impartial, and systematically structured business reports based on provided business data, market trends, and strategic analysis."
        }
        task: "what are the most interesting sites in Tel Aviv?"
        response:
        {
            "server:  "🌍 Travel Agent",
            "agent_role_prompt": "You are a world-travelled AI tour guide assistant. Your main purpose is to draft engaging, insightful, unbiased, and well-structured travel reports on given locations, including history, attractions, and cultural insights."
        }
    """


def generate_summary_prompt(query, data):
    """ Generates the summary prompt for the given question and text.
    Args: question (str): The question to generate the summary prompt for
            text (str): The text to generate the summary prompt for
    Returns: str: The summary prompt for the given question and text
    """

    return f'{data} Using the above text, summarize it based on the following task or query: "{query}". If the ' \
           f'query cannot be answered using the text, YOU MUST summarize the text in short. Include all factual ' \
           f'information such as numbers, stats, quotes, etc if available. '