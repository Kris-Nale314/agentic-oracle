# 🤖 Agentic Oracle

<div align="center">

![Agentic Oracle Banner](https://via.placeholder.com/800x200?text=Agentic+Oracle)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
[![CrewAI](https://img.shields.io/badge/CrewAI-Framework-orange.svg)](https://www.crewai.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)

**AI-Powered Company Intelligence Briefing System**

*Where a crew of AI agents works together to generate insightful company analyses*

</div>

## 🌟 The Vision

Agentic Oracle is both an **educational and functional** AI application that showcases the power, complexity, and potential of multi-agent systems. Too often, we think of AI as a single large model answering questions, but the future may be much more nuanced: specialized AI agents collaborating to solve complex problems, just like human teams.

Our goal is to help data scientists, AI enthusiasts, and business professionals:

1. **Understand** the inner workings of multi-agent AI systems
2. **Visualize** how agents with different specialties collaborate
3. **Experience** the results of this collaboration firsthand
4. **Learn** about the tradeoffs and complexities involved

And while learning all this, actually get useful company analysis insights! Who says education can't be practical?

## ✨ What Makes This Special

Most AI demos focus on showcasing a single model's capabilities. Agentic Oracle takes a different approach:

- **Multi-Agent Architecture**: Specialized AI agents collaborate as a "crew"
- **Tool-Using Agents**: Agents use APIs to gather real data, not just pre-trained knowledge
- **Transparent Process**: You can peek inside the "minds" of the agents to see their thought processes
- **Practical Application**: Generates actually useful company analyses
- **Educational Focus**: Designed to help you understand how agentic systems work "under the hood"

## 🧠 Meet the AI Crew

<table>
  <tr>
    <td align="center" width="200"><h3>💰</h3></td>
    <td><b>Financial Analyst</b><br><i>"Show me the numbers!"</i><br>A no-nonsense Wall Street veteran who digs into financial statements, analyzes metrics, and evaluates company health using hard data.</td>
  </tr>
  <tr>
    <td align="center"><h3>🕵️‍♀️</h3></td>
    <td><b>Profile Researcher</b><br><i>"Let me investigate..."</i><br>A meticulous investigator who builds comprehensive profiles of companies, including business models, competitive positioning, and strategic outlooks.</td>
  </tr>
  <tr>
    <td align="center"><h3>📰</h3></td>
    <td><b>News & Sentiment Analyst</b><br><i>"Here's what people are saying..."</i><br>A former financial journalist with a knack for spotting trends, analyzing sentiment, and identifying key narratives in the media.</td>
  </tr>
  <tr>
    <td align="center"><h3>⚖️</h3></td>
    <td><b>Investment Judge</b><br><i>"After weighing all the evidence..."</i><br>An impartial evaluator who synthesizes all the information to provide an overall investment recommendation.</td>
  </tr>
</table>

## 🚀 What It Does

Agentic Oracle generates comprehensive company briefings on demand. Enter a ticker symbol, and the AI crew will:

1. **Research the company** profile, business model, and competitive positioning
2. **Analyze financial data** including metrics, health indicators, and trends
3. **Review recent news** and gauge market sentiment
4. **Synthesize findings** into an investment recommendation

The output is a detailed briefing organized in a clean, tabbed interface covering all aspects of company analysis.

## 📊 Why Multi-Agent Systems Matter

Traditional AI approaches often use a single large model to handle complex tasks. But multi-agent systems offer several advantages:

- **Specialization**: Each agent can focus on what it does best
- **Data Access**: Agents can use different tools and data sources
- **Collaboration**: Agents can build on each other's findings
- **Transparency**: The process is more understandable than a single "black box"
- **Scalability**: New agents with new capabilities can be added over time

This is closer to how human teams work - specialists collaborating rather than one generalist doing everything.

## 💻 Technical Architecture

<div align="center">
  <img src="https://via.placeholder.com/700x400?text=Agentic+Oracle+Architecture" alt="Agentic Oracle Architecture" width="70%">
</div>

Agentic Oracle is built with:

- **[CrewAI](https://www.crewai.com/)**: Framework for building multi-agent systems
- **[Streamlit](https://streamlit.io/)**: For the interactive web interface
- **[LangChain](https://www.langchain.com/)**: For LLM integration and tools
- **[Financial Modeling Prep API](https://site.financialmodelingprep.com/developer)**: For real financial data
- **[OpenAI API](https://openai.com/)**: Powering the AI agents

Each agent has:
- A defined **role** and **goal**
- A distinct **persona** and backstory
- Access to specific **tools** for gathering information
- The ability to **collaborate** with other agents

## 🏃‍♀️ Getting Started

### Prerequisites

- Python 3.8+
- [Financial Modeling Prep](https://site.financialmodelingprep.com/developer) API key
- [OpenAI](https://beta.openai.com/signup/) API key

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-oracle.git
cd agentic-oracle

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your API keys in a .env file
echo "FMP_API_KEY=your_fmp_api_key" > .env
echo "OPENAI_API_KEY=your_openai_api_key" >> .env

# Launch the app
streamlit run main.py
```

## 👩‍💻 How to Use

1. Enter a company's ticker symbol (e.g., AAPL, MSFT, GOOG)
2. Select an analysis depth:
   - **Quick Assessment**: Faster, less detail (good for initial screening)
   - **Deep Analysis**: More comprehensive (recommended for serious research)
3. Choose an investment style (optional):
   - **Balanced**: Considers all factors equally
   - **Just the Facts**: Emphasizes financials and hard data
   - **News Hound**: Gives more weight to recent news and sentiment
4. Click "Generate Briefing" and watch the AI crew work!
5. Explore the results in different tabs:
   - Overview: Executive summary and key metrics
   - Company Profile: Business model and competitive analysis
   - Financial Analysis: Detailed financial metrics and health assessment
   - News & Sentiment: Recent news and market sentiment analysis
   - Raw Data: For those who want to see the unprocessed agent outputs

## 📚 Educational Value

Agentic Oracle is designed as an educational tool to help understand:

- **Agent Design**: How to craft effective AI agents with clear roles and goals
- **Tool Integration**: How AI can use external tools to gather fresh information
- **Prompt Engineering**: How different prompts affect agent behavior and output
- **Orchestration Patterns**: How to coordinate multiple agents effectively
- **Tradeoffs**: The relationship between analysis depth, speed, and token usage

The app includes educational content explaining these concepts and allows you to experiment with different settings to see their effects.

## 🔍 The Bigger Picture

Beyond company analysis, Agentic Oracle demonstrates a paradigm that could transform how we build AI systems:

- **Division of Labor**: Complex tasks divided among specialized agents
- **Human-Like Collaboration**: Agents that communicate, delegate, and build on each other's work
- **Transparent Reasoning**: See how different perspectives contribute to final outputs
- **Practical Tools**: Systems that combine pre-trained knowledge with real-time data access

This approach may prove more scalable, explainable, and effective than always pushing for bigger single models.

## 🛠️ For Developers

The codebase is structured to be educational and extensible:

```
agentic-oracle/
├── main.py                   # Streamlit UI
├── agents/                   # Agent definitions
│   ├── financial_agent.py
│   ├── profile_agent.py
│   ├── news_agent.py
│   └── investment_judge_agent.py
├── tools/                    # Tools and helpers
│   ├── fmp_tool.py           # Financial Modeling Prep API wrapper
│   └── helper_functions.py   # Core analysis function and utilities
├── judge/                    # Investment judge logic
│   └── investment_judge.py
├── requirements.txt
└── README.md
```

Key design patterns:
- Clear separation between UI and analysis logic
- Modular agent definitions for easy extension
- Centralized `run_analysis` function for orchestration
- Robust error handling and fallback mechanisms

## 🔮 Future Directions

Agentic Oracle is just the beginning. Future enhancements could include:

- **More Specialized Agents**: Legal analysts, ESG evaluators, technical analysts
- **Agent Memory**: Persistent knowledge across sessions
- **Comparative Analysis**: Simultaneous analysis of multiple companies
- **Data Visualization**: Interactive charts and graphics
- **Custom Agent Creation**: UI for designing your own agents
- **Explanations**: Educational content about how each analysis was generated

## 🤝 Contributing

We welcome contributions! If you're interested in improving Agentic Oracle:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-idea`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-idea`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The [CrewAI](https://www.crewai.com/) team for their groundbreaking framework
- [Financial Modeling Prep](https://site.financialmodelingprep.com/developer) for their comprehensive financial data API
- [OpenAI](https://openai.com/) for their powerful language models
- [Streamlit](https://streamlit.io/) for making it easy to build beautiful data apps

---

<div align="center">
  <p><i>Agentic Oracle: Where AI agents collaborate to bring you insights!</i></p>
  <p>
    <a href="https://github.com/yourusername/agentic-oracle">GitHub</a> •
    <a href="https://twitter.com/yourusername">Twitter</a> •
    <a href="https://www.linkedin.com/in/yourusername">LinkedIn</a>
  </p>
</div>