# tools/helper_functions.py - Utility functions for the Agentic Oracle app
import tiktoken
import re
import json
import logging
from typing import Dict, Any, List, Tuple
from crewai import Agent
from crewai.task import TaskOutput


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Check if handlers are already configured to avoid duplicate logs
if not logger.handlers:
    fh = logging.FileHandler('app.log')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    """
    Estimate the number of tokens in a text string for a given model.
    
    Args:
        text: The text to count tokens for
        model_name: The name of the model to use for counting
        
    Returns:
        The estimated number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # Fall back to cl100k_base encoding if model-specific encoding not found
        encoding = tiktoken.get_encoding("cl100k_base")
    
    # Count the tokens
    num_tokens = len(encoding.encode(text))
    return num_tokens

def extract_json_like(text: str) -> Dict[str, Any]:
    """
    Extract a JSON-like dictionary from a string.
    
    Args:
        text: The text to extract JSON from
        
    Returns:
        A dictionary parsed from the JSON-like text, or an empty dict if parsing fails
    """
    if not text or not isinstance(text, str):
        return {}
    
    try:
        # First try direct JSON parsing
        return json.loads(text)
    except json.JSONDecodeError:
        # If direct parsing fails, try to find JSON objects in the string
        try:
            # Look for JSON-like objects enclosed in curly braces
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                json_str = match.group(0)
                # Replace single quotes with double quotes for JSON
                json_str = json_str.replace("'", '"')
                return json.loads(json_str)
        except (json.JSONDecodeError, AttributeError):
            pass
        
        # If all parsing attempts fail, return an empty dict
        return {}

def extract_agent_outputs(results: Any, financial_analyst: Agent, profile_researcher: Agent, news_analyst: Agent) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """
    Extract and parse outputs from the agent results.
    
    Args:
        results: The results from the CrewAI crew execution
        financial_analyst: The Financial Analyst agent
        profile_researcher: The Profile Researcher agent
        news_analyst: The News Analyst agent
        
    Returns:
        Tuple of (financial_analysis, profile_analysis, news_analysis) dictionaries
    """
    financial_analysis_output = {}
    profile_researcher_output = {}
    news_analyst_output = {}
    
    # Initialize with empty dictionaries in case parsing fails
    try:
        # Case 1: Results is a list of TaskOutput objects
        if isinstance(results, list):
            for result in results:
                if hasattr(result, 'agent') and hasattr(result, 'output'):
                    agent_role = result.agent.role
                    output_text = result.output
                    
                    if agent_role == profile_researcher.role:
                        profile_researcher_output = extract_json_like(output_text)
                    elif agent_role == financial_analyst.role:
                        financial_analysis_output = extract_json_like(output_text)
                    elif agent_role == news_analyst.role:
                        news_analyst_output = extract_json_like(output_text)
        
        # Case 2: Results has an output attribute
        elif hasattr(results, 'output'):
            output_text = results.output
            
            # Try to parse the entire output
            all_data = extract_json_like(output_text)
            
            # If that fails, try to extract sections based on headers
            if not all_data:
                # Try to find sections in the text based on headings
                financial_section = re.search(r'Financial Analysis[:\n]+(.*?)(?=Profile Analysis|News Analysis|$)', 
                                             output_text, re.DOTALL | re.IGNORECASE)
                if financial_section:
                    financial_analysis_output = extract_json_like(financial_section.group(1))
                
                profile_section = re.search(r'Profile Analysis[:\n]+(.*?)(?=Financial Analysis|News Analysis|$)', 
                                          output_text, re.DOTALL | re.IGNORECASE)
                if profile_section:
                    profile_researcher_output = extract_json_like(profile_section.group(1))
                
                news_section = re.search(r'News Analysis[:\n]+(.*?)(?=Financial Analysis|Profile Analysis|$)', 
                                        output_text, re.DOTALL | re.IGNORECASE)
                if news_section:
                    news_analyst_output = extract_json_like(news_section.group(1))
        
        # Case 3: Results is a string
        elif isinstance(results, str):
            # Try to find all JSON objects in the string
            json_objects = re.findall(r'\{.*?\}', results, re.DOTALL)
            
            # Try to categorize each JSON object
            for json_str in json_objects:
                try:
                    data = json.loads(json_str.replace("'", '"'))
                    
                    # Categorize based on content
                    if any(key in data for key in ["financial_health", "key_metrics"]):
                        financial_analysis_output = data
                    elif any(key in data for key in ["business_outlook", "industry_position"]):
                        profile_researcher_output = data
                    elif any(key in data for key in ["sentiment", "news_summary"]):
                        news_analyst_output = data
                except (json.JSONDecodeError, TypeError):
                    continue
    except Exception as e:
        logger.error(f"Error extracting agent outputs: {str(e)}")
    
    # Log the extracted data
    logger.info(f"Extracted financial data: {bool(financial_analysis_output)}")
    logger.info(f"Extracted profile data: {bool(profile_researcher_output)}")
    logger.info(f"Extracted news data: {bool(news_analyst_output)}")
    
    return financial_analysis_output, profile_researcher_output, news_analyst_output