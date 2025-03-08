# 🚀 Agentic Oracle

**Where AI agents work together to make sense of messy financial data**

## 💡 The Vision

**Data is messy, and AI is not magic.** 

Agentic Oracle is an educational platform that pulls back the curtain on "AI magic" to show you what's *actually* happening when multiple AI agents collaborate to solve real problems with real data.

> *"Your data strategy is as important as your solution architecture."*

Before you roll your eyes at yet another "agentic AI" project, hear us out - this is actually a big deal. Multi-agent AI systems represent a fundamental shift in how we design, build, test, and deploy AI solutions. Understanding how these systems work helps you:

1. **Make better architectural decisions** for your own AI implementations
2. **See through the snake oil** being peddled by AI vendors
3. **Appreciate the critical role** of data preparation in any AI system
4. **Witness firsthand** how specialized agents can outperform a single model

All while exploring practical financial use cases that showcase these principles in action!

## 🔍 What We're Exploring

Agentic Oracle tackles common challenges that arise when working with unstructured financial data:

- **Document Boundary Detection**: When did the Q1 earnings call end and the analyst report begin?
- **Intelligent Document Processing**: Different document types need different handling strategies
- **Context-Aware Analysis**: How temporal and entity references shift meaning across documents
- **Information Synthesis**: Turning scattered insights into cohesive understanding

Through these lenses, we explore fundamental AI concepts that every modern practitioner should understand:

```
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│                        │      │                        │      │                        │
│   Data Preparation     │─────►│   Agent Orchestration  │─────►│   Insight Synthesis    │
│                        │      │                        │      │                        │
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘
```


agentic-oracle/
├── data/
│   └── dell_financial_dataset.json
├── agents/
│   ├── __init__.py
│   ├── financial_analyst.py
│   ├── profile_researcher.py
│   ├── news_analyst.py
│   └── boundary_detector.py
├── judge/
│   ├── __init__.py
│   └── investment_judge.py
├── processors/
│   ├── __init__.py
│   ├── text_processor.py
│   ├── chunking_strategies.py
│   └── embedding_generator.py
├── utils/
│   ├── __init__.py
│   ├── openai_client.py
│   └── evaluation.py
├── tests/
│   ├── __init__.py
│   ├── test_boundary_detection.py
│   ├── test_document_classification.py
│   └── test_analysis.py
├── analysis.py  # CrewAI orchestration and task definitions
├── orchestration.py  # Higher-level orchestration for Streamlit
├── main.py  # Streamlit app
├── requirements.txt
└── README.md



## 🧠 Meet the AI Crew

<table>
  <tr>
    <td align="center" width="200"><h3>🔍</h3></td>
    <td><b>Boundary Detective</b><br><i>"I can see where these documents have been stitched together!"</i><br>Specializes in detecting document boundaries, identifying format shifts, and classifying document types in mixed content.</td>
  </tr>
  <tr>
    <td align="center"><h3>💰</h3></td>
    <td><b>Financial Analyst</b><br><i>"Let me crunch these numbers..."</i><br>Extracts and analyzes financial metrics, trends, and performance indicators from earnings calls and reports.</td>
  </tr>
  <tr>
    <td align="center"><h3>📰</h3></td>
    <td><b>News Analyst</b><br><i>"Here's what the market is saying..."</i><br>Processes news articles, social sentiment, and market narratives to provide context around financial data.</td>
  </tr>
  <tr>
    <td align="center"><h3>⚖️</h3></td>
    <td><b>Investment Judge</b><br><i>"After weighing all the evidence..."</i><br>Synthesizes information from all sources to provide balanced, contextual insights and recommendations.</td>
  </tr>
</table>

## 🛠️ What Makes This Different

Most AI demos show you the output of a magical black box. We're showing you:

- **The Data Journey**: From raw, messy input to structured, actionable insights
- **Agent Specialization**: How targeted expertise leads to better results than one-size-fits-all models
- **Orchestration Mechanics**: The how and why of agent collaboration and communication
- **Failure Modes**: What happens when agents misinterpret or hallucinate, and how to prevent it

## 🔬 Educational Use Cases

Agentic Oracle includes educational modules demonstrating:

1. **Smart Chunking vs. Basic RAG**: Why document understanding matters before embedding
2. **Boundary Detection Challenge**: Can your system tell where one document ends and another begins?
3. **Mixed Context Analysis**: Handling multi-company, multi-timeframe document collections
4. **Agent Communication Patterns**: Visualizing how information flows between agents

## 🔧 Technical Stack

This project is built with:

- **[CrewAI](https://www.crewai.com/)**: Framework for building multi-agent systems
- **[OpenAI](https://openai.com/)**: GPT-3.5 Turbo for cost-effective agent implementation
- **[Streamlit](https://streamlit.io/)**: For the interactive web interface
- **[Financial Modeling Prep API](https://site.financialmodelingprep.com/developer)**: For clean financial reference data

## 👨‍💻 Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-oracle.git
cd agentic-oracle

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run main.py
```

## 🤝 Contribute

Interested in contributing? We're looking for help with:

- Additional agent specializations
- New document types and processing strategies
- Improved evaluation metrics
- Educational visualizations

Check out the [issues](https://github.com/yourusername/agentic-oracle/issues) to get started!

---

*Made with ❤️ by Kris Naleszkiewicz | [LinkedIn](https://www.linkedin.com/in/kris-nale314/) | [Medium](https://medium.com/@kris_nale314)*