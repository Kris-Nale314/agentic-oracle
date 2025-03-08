# agents/investment_judge_agent.py
from crewai import Agent
from langchain_community.chat_models import ChatOpenAI
from textwrap import dedent

def create_investment_judge_agent(model_name="gpt-3.5-turbo", temperature=0.1):
    """
    Creates an Investment Judge agent.
    """
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    return Agent(
        role="Investment Judge",
        goal=dedent("""Provide a well-reasoned investment rating (1-5) and justification
                    for a company, based on inputs from other agents. Output MUST be in JSON format."""),
        backstory=dedent("""You are an impartial judge with expertise in finance and market analysis.
                        You receive structured reports from other analysts and synthesize them
                        into a final investment rating and justification. Your output must be in JSON format."""),
        verbose=True,
        allow_delegation=False,  # Judge doesn't delegate
        llm=llm
    )