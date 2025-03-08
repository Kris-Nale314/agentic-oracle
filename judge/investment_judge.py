# judge/investment_judge.py
import streamlit as st
import json
import re
import logging
from textwrap import dedent
from typing import Dict, Any, Union

logger = logging.getLogger(__name__)

def get_judge_prompt(investment_style: str, ticker: str, financial_analysis_output: Dict[str, Any], profile_researcher_output: Dict[str, Any], news_analyst_output: Dict[str, Any]) -> str:
    """Generates the prompt for the Investment Judge agent."""

    prompt = f"""You are an Investment Judge, responsible for providing an investment rating for {ticker} based on the provided information.
    User Preference: {investment_style}

    Base your rating on these factors according to the user's preference:
     - Just the Facts: Base it solely on the Financial Analysis.
     - Balanced: Base it on the Financial Analysis, Company Profile, and News Sentiment.
     - News Hound: Base it primarily on the News Sentiment.

    Financial Analysis:
    {financial_analysis_output}

    Company Profile:
    {profile_researcher_output}

    News Sentiment:
    {news_analyst_output}

    Based on this information, provide your investment rating as one of: STRONG BUY, BUY, HOLD, SELL, or STRONG SELL.
    Also provide your confidence level (High/Medium/Low) and a concise justification for your rating.
    
    Output in this JSON format:
    {{
     "rating": "your rating (STRONG BUY, BUY, HOLD, SELL, or STRONG SELL)",
     "confidence": "High/Medium/Low",
     "justification": "Your detailed justification here"
    }}
    """
    return dedent(prompt)


def process_judge_output(judge_results: Any) -> None:
    """
    Processes and displays the output from the Investment Judge.
    Now handles different types of results from CrewAI.
    """
    try:
        # Extract the judge output based on different possible return types
        judge_output = None
        
        # Log the type of judge_results for debugging
        logger.info(f"Judge results type: {type(judge_results)}")
        
        # Case 1: judge_results is a list with TaskOutput objects
        if isinstance(judge_results, list) and len(judge_results) > 0:
            if hasattr(judge_results[0], 'output'):
                judge_output = judge_results[0].output
                logger.info("Extracted output from list of TaskOutput objects")
        
        # Case 2: judge_results has a direct 'output' attribute
        elif hasattr(judge_results, 'output'):
            judge_output = judge_results.output
            logger.info("Extracted output from object with 'output' attribute")
        
        # Case 3: judge_results is the raw string output
        elif isinstance(judge_results, str):
            judge_output = judge_results
            logger.info("Judge results is already a string")
        
        # Case 4: judge_results has some other structure
        else:
            # Try to convert to string
            judge_output = str(judge_results)
            logger.info("Converted judge results to string")
        
        # Try to parse the JSON
        try:
            # If we have a string that contains JSON
            if isinstance(judge_output, str):
                # Try to find JSON within the string if it's not pure JSON
                json_match = re.search(r'(\{.*\})', judge_output, re.DOTALL)
                if json_match:
                    judge_json = json.loads(json_match.group(1))
                    logger.info("Extracted JSON from string using regex")
                else:
                    # Try parsing the whole string
                    judge_json = json.loads(judge_output)
                    logger.info("Parsed whole string as JSON")
            else:
                # If it's already a dict
                judge_json = judge_output if isinstance(judge_output, dict) else {"error": "Unable to parse output"}
            
            # Extract values from JSON
            rating = judge_json.get("rating", "N/A")
            confidence = judge_json.get("confidence", "Medium")
            justification = judge_json.get("justification", "No justification provided.")
            
            # Create a visually appealing display
            col1, col2 = st.columns([1, 4])
            
            with col1:
                # Rating display with appropriate color
                if rating.upper() in ["STRONG BUY", "BUY", "5", "4"]:
                    st.success(f"### {rating}")
                elif rating.upper() in ["HOLD", "3"]:
                    st.warning(f"### {rating}")
                elif rating.upper() in ["SELL", "STRONG SELL", "2", "1"]:
                    st.error(f"### {rating}")
                else:
                    st.info(f"### {rating}")
                
                st.caption(f"Confidence: {confidence}")
            
            with col2:
                st.markdown("### Investment Analysis")
                st.markdown(justification)
            
            # Display full JSON for transparency
            with st.expander("View Complete Investment Analysis"):
                st.json(judge_json)
                
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing investment judge output as JSON: {e}")
            st.error("Unable to parse investment analysis output as JSON.")
            st.markdown("### Raw Investment Analysis")
            st.markdown(judge_output)
            
    except Exception as e:
        logger.error(f"Error processing investment judge output: {e}", exc_info=True)
        st.error(f"Error processing investment analysis: {str(e)}")
        st.markdown("### Raw Investment Judge Output")
        st.markdown(str(judge_results))