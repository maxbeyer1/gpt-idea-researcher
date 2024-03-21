from datetime import datetime


def generate_idea_research_queries_prompt(idea):
    return f'Generate research queries for the idea: "{idea}". Include queries related to market research, competitors, demand, features, viability, resources, tech stack, etc.'


def generate_idea_report_prompt(idea):
    return f'Generate a detailed report for the idea: "{idea}". The report should cover market research, competitors, demand, features, viability, resources, tech stack, etc. Use the current date: {datetime.now().strftime("%B %d, %Y")}.'


def get_report_by_type(report_type):
    report_type_mapping = {
        'idea_report': generate_idea_report_prompt,
        'idea_research_queries': generate_idea_research_queries_prompt
    }
    return report_type_mapping.get(report_type, lambda: 'Invalid report type')


def generate_research_queries(idea):
    queries = [
        f'What is the market size for {idea}?',
        f'Who are the competitors for {idea}?',
        f'What is the demand for {idea}?',
        f'What features should {idea} have?',
        f'Is {idea} viable?',
        f'What resources are needed for {idea}?',
        f'What tech stack should be used for {idea}?',
    ]
    return queries


def generate_idea_report(idea):
    queries = generate_research_queries(idea)
    report = ''
    for query in queries:
        report += f'{query}\n'
    return report