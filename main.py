# main.py - Streamlit interface for Agentic Oracle
import os
import time
import json
import streamlit as st
from dotenv import load_dotenv
import logging

# Disable CrewAI telemetry to avoid SSL certificate issues
os.environ["CREWAI_TRACING"] = "false"
os.environ["OPENAI_TELEMETRY"] = "false"

# Load environment variables
load_dotenv()
from tools.fmp_tool import FMPTool
FMPTool()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("agentic_oracle")

# Import the analysis function
from analysis import run_company_analysis
from judge.investment_judge import process_judge_output

# --- Streamlit App ---
def main():
    # Configure the page
    st.set_page_config(
        page_title="Agentic Oracle: Company Intelligence",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize session state
    if "results" not in st.session_state:
        st.session_state.results = None
    if "ticker_history" not in st.session_state:
        st.session_state.ticker_history = []
    
    # App Header
    st.title("🤖 Agentic Oracle")
    st.subheader("AI-Powered Company Intelligence Briefing")
    
    # Sidebar configuration
    with st.sidebar:
        st.title("Analysis Settings")
        
        # Model selection
        model = st.selectbox(
            "AI Model",
            ["gpt-3.5-turbo", "gpt-4"],
            index=0,
            help="GPT-4 provides higher quality but costs more tokens."
        )
        
        # Analysis depth
        depth = st.radio(
            "Analysis Depth",
            ["Quick Assessment", "Deep Analysis"],
            index=0,
            help="Quick is faster, Deep provides more detail."
        )
        
        # Investment style
        investment_style = st.radio(
            "Investment Style",
            ["Balanced", "Just the Facts", "News Hound"],
            index=0,
            help="How to weight different factors in the investment recommendation."
        )
        
        # More options in an expander
        with st.expander("Advanced Options"):
            # Agent temperatures
            st.subheader("Agent Creativity")
            financial_temp = st.slider("Financial Analyst", 0.0, 1.0, 0.3, 0.1)
            profile_temp = st.slider("Profile Researcher", 0.0, 1.0, 0.5, 0.1)
            news_temp = st.slider("News Analyst", 0.0, 1.0, 0.7, 0.1)
            
            # Process type
            process_type = st.selectbox(
                "Agent Collaboration",
                ["Sequential", "Hierarchical"],
                index=0,
                help="How agents work together."
            )
            
            # API rate limit
            max_rpm = st.number_input("API Rate Limit", min_value=3, max_value=30, value=10)
            
            # Verbose toggle
            verbose = st.checkbox("Show Agent Thought Process", value=False)
        
        # Educational content in an expander
        with st.expander("Meet the AI Crew"):
            st.markdown("""
            ### Your AI Analysis Team
            
            **🧮 Financial Analyst**  
            *A Wall Street veteran focused on numbers and metrics*
            
            **🔍 Profile Researcher**  
            *An industry expert who investigates business models and competition*
            
            **📰 News Analyst**  
            *A former journalist who tracks media coverage and sentiment*
            
            **⚖️ Investment Judge**  
            *An experienced advisor who weighs evidence and makes recommendations*
            """)
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker = st.text_input("Enter Company Ticker Symbol", placeholder="e.g., AAPL, MSFT, GOOG").upper()
    with col2:
        analyze_button = st.button(
            "Generate Briefing", 
            type="primary", 
            use_container_width=True,
            disabled=not ticker
        )
    
    # Educational content
    with st.expander("🧠 Learn About Multi-Agent AI Systems"):
        st.markdown("""
        **Agentic Oracle** demonstrates a core concept in AI: multi-agent systems. 
        
        Instead of using a single large model to do everything, we use multiple specialized AI agents, 
        each with their own role, expertise, and access to different tools. This approach:
        
        1. **Mirrors human teams** - Specialists collaborate rather than one generalist doing everything
        2. **Shows division of labor** - Each agent handles what it does best
        3. **Demonstrates tool use** - Agents actively gather fresh data rather than relying solely on training
        4. **Illustrates collaboration** - Agents build on each other's work to reach better conclusions
        
        Watch as the agents work together to analyze the company you've selected!
        """)
    
    # Check for API keys
    if not os.environ.get("FMP_API_KEY") or not os.environ.get("OPENAI_API_KEY"):
        st.error("❌ API keys (FMP_API_KEY and OPENAI_API_KEY) must be set in your .env file.")
        return
    
    # Run analysis when button is clicked
    if analyze_button and ticker:
        # Clear previous results
        st.session_state.results = None
        
        # Set up progress indicators
        progress_area = st.empty()
        with progress_area.container():
            st.markdown(f"### Analyzing {ticker}...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Show progress updates
            status_text.markdown("🤖 **Initializing AI agents...**")
            progress_bar.progress(10)
            time.sleep(0.5)
            
            # Configure agent temperatures
            temps = {
                "financial": financial_temp,
                "profile": profile_temp,
                "news": news_temp
            }
            
            # Convert depth radio button to the format expected by the analysis function
            depth_value = "deep" if depth == "Deep Analysis" else "quick"
            
            # Progress update
            status_text.markdown("🔍 **Agents gathering company data...**")
            progress_bar.progress(30)
            
            try:
                # Run the analysis
                results = run_company_analysis(
                    ticker=ticker,
                    model=model,
                    depth=depth_value,
                    process_type=process_type,
                    temps=temps,
                    investment_style=investment_style,
                    max_rpm=max_rpm,
                    verbose=verbose
                )
                
                # Update progress
                status_text.markdown("📊 **Processing analysis results...**")
                progress_bar.progress(80)
                time.sleep(0.5)
                
                # Store results in session state
                st.session_state.results = results
                
                # Add to ticker history if not already there
                if ticker not in st.session_state.ticker_history:
                    st.session_state.ticker_history.append(ticker)
                
                # Complete progress
                status_text.markdown("✅ **Analysis complete!**")
                progress_bar.progress(100)
                time.sleep(0.5)
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                logger.error(f"Analysis error: {str(e)}", exc_info=True)
            
            # Clear progress area
            progress_area.empty()
        
        # Check for errors in results
        if "error" in st.session_state.results:
            st.error(st.session_state.results["error"])
        else:
            # Display success message
            st.success(f"Analysis of {ticker} completed in {st.session_state.results['execution_time']:.1f} seconds")
            
            # Display results in tabs
            display_results(st.session_state.results)
    
    # If we have results in session state, display them
    elif st.session_state.results is not None:
        display_results(st.session_state.results)
    
    # Display ticker history as chips
    if st.session_state.ticker_history:
        st.markdown("### Previously Analyzed Companies")
        cols = st.columns(6)
        for i, prev_ticker in enumerate(st.session_state.ticker_history):
            col_idx = i % 6
            if cols[col_idx].button(prev_ticker, key=f"history_{prev_ticker}"):
                # Re-analyze this ticker
                st.session_state.results = None
                st.rerun()

def display_results(results):
    """Display analysis results in a tabbed interface"""
    # Create tabs for different sections
    tabs = st.tabs(["Overview", "Company Profile", "Financial Analysis", "News & Sentiment", "Raw Data"])
    
    # Overview tab
    with tabs[0]:
        st.header(f"Executive Summary: {results.get('ticker', '')}")
        
        # Investment recommendation
        if "investment_recommendation" in results:
            st.subheader("Investment Recommendation")
            process_judge_output(results["investment_recommendation"])
        
        # Key metrics from each analysis
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if isinstance(results.get("profile_analysis"), dict):
                outlook = results["profile_analysis"].get("business_outlook", "Unknown")
                st.metric("Business Outlook", outlook)
                
        with col2:
            if isinstance(results.get("financial_analysis"), dict):
                health = results["financial_analysis"].get("financial_health", "Unknown")
                st.metric("Financial Health", health)
                
        with col3:
            if isinstance(results.get("news_analysis"), dict):
                sentiment = results["news_analysis"].get("sentiment", "Unknown")
                st.metric("News Sentiment", sentiment)
        
        # Analysis stats
        st.markdown("---")
        st.caption(f"Analysis completed in {results.get('execution_time', 0):.1f} seconds using {results.get('config', {}).get('model', '')}.")
        st.caption(f"Approximate token usage: {results.get('token_usage', 'Unknown')}")
    
    # Company Profile tab
    with tabs[1]:
        st.header("Company Profile Analysis")
        if "profile_analysis" in results and isinstance(results["profile_analysis"], dict):
            # Display summary if available
            if "profile_summary" in results["profile_analysis"]:
                st.subheader("Summary")
                st.markdown(results["profile_analysis"]["profile_summary"])
            
            # Business model
            if "business_model" in results["profile_analysis"]:
                st.subheader("Business Model")
                st.markdown(results["profile_analysis"]["business_model"])
            
            # Competitive analysis
            if "competitive_analysis" in results["profile_analysis"]:
                st.subheader("Competitive Position")
                st.markdown(results["profile_analysis"]["competitive_analysis"])
            
            # Risks and opportunities
            if "key_risks" in results["profile_analysis"] or "key_opportunities" in results["profile_analysis"]:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Key Risks")
                    risks = results["profile_analysis"].get("key_risks", [])
                    for risk in risks:
                        st.markdown(f"- {risk}")
                
                with col2:
                    st.subheader("Key Opportunities")
                    opportunities = results["profile_analysis"].get("key_opportunities", [])
                    for opportunity in opportunities:
                        st.markdown(f"- {opportunity}")
            
            # SWOT analysis (for deep analysis)
            if "swot_analysis" in results["profile_analysis"]:
                st.subheader("SWOT Analysis")
                swot = results["profile_analysis"]["swot_analysis"]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Strengths**")
                    for item in swot.get("strengths", []):
                        st.markdown(f"- {item}")
                    
                    st.markdown("**Weaknesses**")
                    for item in swot.get("weaknesses", []):
                        st.markdown(f"- {item}")
                
                with col2:
                    st.markdown("**Opportunities**")
                    for item in swot.get("opportunities", []):
                        st.markdown(f"- {item}")
                    
                    st.markdown("**Threats**")
                    for item in swot.get("threats", []):
                        st.markdown(f"- {item}")
            
            # Raw JSON
            with st.expander("View Raw Profile Data"):
                st.json(results["profile_analysis"])
        else:
            st.info("No company profile data available")
    
    # Financial Analysis tab
    with tabs[2]:
        st.header("Financial Analysis")
        if "financial_analysis" in results and isinstance(results["financial_analysis"], dict):
            # Display summary if available
            if "financial_summary" in results["financial_analysis"]:
                st.subheader("Summary")
                st.markdown(results["financial_analysis"]["financial_summary"])
            
            # Key metrics
            if "key_metrics" in results["financial_analysis"]:
                st.subheader("Key Financial Metrics")
                metrics = results["financial_analysis"]["key_metrics"]
                
                # Determine number of columns based on metrics count
                num_metrics = len(metrics)
                num_cols = min(4, max(2, num_metrics))
                cols = st.columns(num_cols)
                
                # Display metrics
                for i, (key, value) in enumerate(metrics.items()):
                    col_idx = i % num_cols
                    display_name = key.replace("_", " ").title()
                    cols[col_idx].metric(display_name, value)
            
            # Analysis sections
            for section in ["profitability_analysis", "growth_analysis", "balance_sheet_analysis",
                           "valuation_analysis", "capital_allocation_analysis"]:
                if section in results["financial_analysis"]:
                    st.subheader(section.replace("_", " ").title())
                    st.markdown(results["financial_analysis"][section])
            
            # Raw JSON
            with st.expander("View Raw Financial Data"):
                st.json(results["financial_analysis"])
        else:
            st.info("No financial analysis data available")
    
    # News & Sentiment tab
    with tabs[3]:
        st.header("News & Sentiment Analysis")
        if "news_analysis" in results and isinstance(results["news_analysis"], dict):
            # Display sentiment
            if "sentiment" in results["news_analysis"]:
                sentiment = results["news_analysis"]["sentiment"]
                if sentiment.lower() == "positive":
                    st.success(f"Overall Sentiment: {sentiment}")
                elif sentiment.lower() == "negative":
                    st.error(f"Overall Sentiment: {sentiment}")
                else:
                    st.warning(f"Overall Sentiment: {sentiment}")
            
            # News summary
            if "news_summary" in results["news_analysis"]:
                st.subheader("News Summary")
                st.markdown(results["news_analysis"]["news_summary"])
            
            # Key themes
            if "key_themes" in results["news_analysis"]:
                st.subheader("Key Themes")
                themes = results["news_analysis"]["key_themes"]
                for theme in themes:
                    st.markdown(f"- {theme}")
            
            # Notable events
            if "notable_events" in results["news_analysis"]:
                st.subheader("Notable Events")
                events = results["news_analysis"]["notable_events"]
                for event in events:
                    st.markdown(f"- {event}")
            
            # Additional sections for deep analysis
            for section in ["analyst_consensus", "social_media_sentiment", 
                          "potential_stock_impact", "sentiment_trend"]:
                if section in results["news_analysis"]:
                    st.subheader(section.replace("_", " ").title())
                    st.markdown(results["news_analysis"][section])
            
            # Raw JSON
            with st.expander("View Raw News Data"):
                st.json(results["news_analysis"])
        else:
            st.info("No news analysis data available")
    
    # Raw Data tab
    with tabs[4]:
        st.header("Raw Analysis Data")
        
        # Show all raw data in expandable sections
        if "raw_outputs" in results:
            with st.expander("Initial Crew Results"):
                st.code(results["raw_outputs"].get("initial_results", "No data"))
            
            with st.expander("Investment Judge Results"):
                st.code(results["raw_outputs"].get("judge_results", "No data"))
        
        # Links to logs and additional info
        st.markdown("---")
        st.caption("For detailed execution logs, check the `app.log` file in your project directory.")

        # Information about CrewAI
        st.markdown("""
        ### About Multi-Agent Systems
        
        This analysis was performed by a "crew" of specialized agents using the **CrewAI** framework.
        Each agent performs specific tasks, uses tools to gather information, and collaborates with other agents.
        
        The analysis process:
        1. Agents gather information using the Financial Modeling Prep API
        2. Each agent analyzes data in its area of expertise
        3. The Investment Judge combines all analyses into a final recommendation
        
        This approach demonstrates how multiple specialized models can be more effective than 
        a single model attempting to do everything.
        """)

if __name__ == "__main__":
    main()