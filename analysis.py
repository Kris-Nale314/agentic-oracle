# analysis.py - Core multi-agent analysis functionality
import os
import time
import logging
from typing import Dict, Any, List, Optional
from textwrap import dedent
from tools.fmp_tool import FMPTool

# Disable CrewAI telemetry to avoid SSL certificate issues
os.environ["CREWAI_TRACING"] = "false"
os.environ["OPENAI_TELEMETRY"] = "false"

# Import CrewAI and LangChain components
from crewai import Crew, Agent, Task, Process
from langchain.tools import Tool
from langchain_community.chat_models import ChatOpenAI

# Configure logging
logger = logging.getLogger("agentic_oracle")

def run_company_analysis(
    ticker: str,
    model: str = "gpt-3.5-turbo",
    depth: str = "quick",
    process_type: str = "sequential",
    temps: Optional[Dict[str, float]] = None,
    investment_style: str = "Balanced",
    max_rpm: int = 10,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Run a multi-agent analysis on a company using CrewAI.
    
    Args:
        ticker: Company stock ticker symbol
        model: LLM model to use (gpt-3.5-turbo or gpt-4)
        depth: Analysis depth (quick or deep)
        process_type: Agent collaboration style (sequential or hierarchical)
        temps: Temperature settings for each agent 
               e.g. {"financial": 0.3, "profile": 0.5, "news": 0.7}
        investment_style: Investment style preference
        max_rpm: Maximum API requests per minute
        verbose: Whether to show verbose agent output
        
    Returns:
        Dict containing analysis results from all agents
    """
    logger.info(f"Starting analysis for {ticker} using {model}")
    start_time = time.time()
    
    # Set default temperatures
    if temps is None:
        if depth == "deep":
            temps = {"financial": 0.3, "profile": 0.5, "news": 0.7}
        else:  # quick
            temps = {"financial": 0.2, "profile": 0.3, "news": 0.5}
    
    try:
        # Initialize FMP Tool with rate limiting
        from tools.fmp_tool import FMPTool
        fmp_tool = FMPTool(max_rpm=max_rpm)
        logger.info(f"FMP Tool initialized with max_rpm={max_rpm}")
        
        # Create tools for accessing financial data
        company_profile_tool = Tool(
            name="Company Profile Tool",
            func=fmp_tool.get_company_profile,
            description="Fetches company profile information. Input should be a ticker symbol."
        )
        
        financial_data_tool = Tool(
            name="Financial Data Tool",
            func=fmp_tool.get_key_financials,
            description="Fetches key financial metrics for a company. Input should be a ticker symbol."
        )
        
        stock_quote_tool = Tool(
            name="Stock Quote Tool",
            func=fmp_tool.get_stock_quote,
            description="Fetches current stock price and related metrics. Input should be a ticker symbol."
        )
        
        news_sentiment_tool = Tool(
            name="News Sentiment Tool",
            func=fmp_tool.get_news_sentiment,
            description="Fetches recent news and market sentiment. Input should be a ticker symbol."
        )
        
        # Define tool sets
        profile_tools = [company_profile_tool]
        financial_tools = [financial_data_tool, stock_quote_tool]
        news_tools = [news_sentiment_tool]
        all_tools = profile_tools + financial_tools + news_tools
        
        # Import agent creation functions
        from agents.financial_agent import create_financial_agent
        from agents.profile_agent import create_profile_agent
        from agents.news_agent import create_news_agent
        from agents.investment_judge_agent import create_investment_judge_agent
        
        # Create specialized agents
        logger.info("Creating specialized agents")
        financial_analyst = create_financial_agent(
            tools=all_tools if depth == "deep" else financial_tools,
            model_name=model,
            temperature=temps["financial"]
        )
        
        profile_researcher = create_profile_agent(
            tools=all_tools if depth == "deep" else profile_tools,
            model_name=model,
            temperature=temps["profile"]
        )
        
        news_analyst = create_news_agent(
            tools=all_tools if depth == "deep" else news_tools,
            model_name=model,
            temperature=temps["news"]
        )
        
        # Determine if we're doing deep analysis
        is_deep = depth == "deep"
        
        # Create tasks for each agent with appropriate prompts
        profile_task_description = f"""
        Gather and analyze a comprehensive profile of {ticker}.
        Research the company's business model, products/services, market position, 
        competitive advantages, and any notable risks or opportunities.
        
        {'''Also analyze industry trends, regulatory environment,
        and long-term strategic positioning.''' if is_deep else ''}
        
        Output should include:
        - Company overview (including name, industry, sector)
        - Business model analysis
        - Competitive positioning
        {'''- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
        - Future outlook''' if is_deep else ''}
        
        Output should be in this JSON-like format:
        {{
            "business_outlook": "Positive/Neutral/Negative/Unknown",
            "industry_position": "Leader/Challenger/Niche Player/Unknown",
            "profile_summary": "Concise summary here",
            "business_model": "Detailed analysis here",
            "competitive_analysis": "Competitive positioning details",
            "key_risks": ["Risk 1", "Risk 2"],
            "key_opportunities": ["Opportunity 1", "Opportunity 2"]
            {''', "swot_analysis": {
                "strengths": ["Strength 1", "Strength 2"],
                "weaknesses": ["Weakness 1", "Weakness 2"],
                "opportunities": ["Opportunity 1", "Opportunity 2"],
                "threats": ["Threat 1", "Threat 2"]
            },
            "future_outlook": "Detailed outlook analysis"''' if is_deep else ''}
        }}
        """
        
        financial_task_description = f"""
        Perform a comprehensive financial analysis of {ticker}.
        
        Analyze:
        - Profitability metrics (margins, ROE, ROA)
        - Growth rates (revenue, earnings, cash flow)
        - Balance sheet health (debt levels, liquidity)
        - Valuation metrics (P/E, P/S, EV/EBITDA)
        - Cash flow generation and usage
        
        {'''- Include trend analysis over 3-5 years
        - Compare to industry benchmarks
        - Analyze dividend and share repurchase history
        - Evaluate capital allocation strategy''' if is_deep else ''}
        
        Output should be in this JSON-like format:
        {{
            "financial_health": "Strong/Moderate/Weak/Unknown",
            "key_metrics": {{
                "pe_ratio": value,
                "revenue_growth": value,
                "profit_margin": value,
                "debt_to_equity": value,
                "return_on_equity": value
                {''', "dividend_yield": value,
                "payout_ratio": value,
                "free_cash_flow": value,
                "ebitda_margin": value''' if is_deep else ''}
            }},
            "financial_summary": "Concise summary here",
            "profitability_analysis": "Details on profitability",
            "growth_analysis": "Details on growth trends",
            "balance_sheet_analysis": "Details on balance sheet health"
            {''', "valuation_analysis": "Details on valuation metrics",
            "capital_allocation_analysis": "Details on how the company allocates capital",
            "industry_comparison": "Comparison with industry peers",
            "trend_analysis": "Analysis of key financial trends over time"''' if is_deep else ''}
        }}
        """
        
        news_task_description = f"""
        Analyze recent news, market sentiment, and media coverage for {ticker}.
        
        Your analysis should include:
        - Summary of major recent news events
        - Overall sentiment assessment (positive, neutral, negative)
        - Key narrative themes in media coverage
        - Impact of recent events on company perception
        
        {'''Also analyze:
        - Social media sentiment trends
        - Analyst opinions and consensus
        - Potential impact of news on stock price and business performance''' if is_deep else ''}
        
        Output should be in this JSON-like format:
        {{
            "sentiment": "Positive/Neutral/Negative/Unknown",
            "news_summary": "Concise summary here",
            "key_themes": ["Theme 1", "Theme 2"],
            "notable_events": ["Event 1", "Event 2"]
            {''', "analyst_consensus": "Details on analyst opinions",
            "social_media_sentiment": "Analysis of social media trends",
            "potential_stock_impact": "Analysis of potential news impact on stock",
            "sentiment_trend": "How sentiment has changed recently"''' if is_deep else ''}
        }}
        """
        
        # Create tasks
        logger.info("Creating agent tasks")
        profile_task = Task(
            description=dedent(profile_task_description),
            agent=profile_researcher,
            expected_output="Comprehensive company profile analysis"
        )
        
        financial_task = Task(
            description=dedent(financial_task_description),
            agent=financial_analyst,
            expected_output="Detailed financial analysis"
        )
        
        news_task = Task(
            description=dedent(news_task_description),
            agent=news_analyst,
            expected_output="News and sentiment analysis"
        )
        
        # Set up the process type
        process = Process.hierarchical if process_type.lower() == "hierarchical" else Process.sequential
        
        # Create the initial crew for gathering data and analyzing
        logger.info(f"Creating crew with {process_type} process")
        initial_crew = Crew(
            agents=[profile_researcher, financial_analyst, news_analyst],
            tasks=[profile_task, financial_task, news_task],
            verbose=verbose,
            process=process
        )
        
        # Execute the crew
        logger.info("Starting crew execution")
        initial_results = initial_crew.kickoff()
        logger.info("Crew execution completed")
        
        # Extract outputs from the results using helper functions
        from tools.helper_functions import extract_agent_outputs
        financial_analysis, profile_analysis, news_analysis = extract_agent_outputs(
            initial_results, financial_analyst, profile_researcher, news_analyst
        )
        logger.info("Agent outputs extracted")
        
        # Create and run the investment judge
        from judge.investment_judge import get_judge_prompt
        investment_judge = create_investment_judge_agent(
            model_name=model,
            temperature=0.1
        )
        
        judge_prompt = get_judge_prompt(
            investment_style, ticker, financial_analysis, profile_analysis, news_analysis
        )
        
        judge_task = Task(
            description=judge_prompt,
            agent=investment_judge,
            expected_output="Investment rating and justification"
        )
        
        judge_crew = Crew(
            agents=[investment_judge],
            tasks=[judge_task],
            verbose=verbose,
            process=Process.sequential
        )
        
        logger.info("Starting investment judge execution")
        judge_results = judge_crew.kickoff()
        logger.info("Investment judge execution completed")
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Estimate token usage (simple approximation)
        from tools.helper_functions import count_tokens
        estimated_tokens = count_tokens(str(initial_results), model) + count_tokens(str(judge_results), model)
        
        # Return the complete results package
        return {
            "ticker": ticker,
            "profile_analysis": profile_analysis,
            "financial_analysis": financial_analysis,
            "news_analysis": news_analysis,
            "investment_recommendation": judge_results,
            "execution_time": execution_time,
            "token_usage": estimated_tokens,
            "config": {
                "model": model,
                "depth": depth,
                "process_type": process_type,
                "investment_style": investment_style
            },
            "raw_outputs": {
                "initial_results": str(initial_results),
                "judge_results": str(judge_results)
            }
        }
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        execution_time = time.time() - start_time
        
        # Return error information
        return {
            "ticker": ticker,
            "error": f"Analysis failed: {str(e)}",
            "execution_time": execution_time,
            "config": {
                "model": model,
                "depth": depth,
                "process_type": process_type,
                "investment_style": investment_style
            }
        }