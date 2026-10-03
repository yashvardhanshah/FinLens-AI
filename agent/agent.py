import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from agent.tools import get_stock_data, search_news, search_document

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def run_agent(company_name: str, ticker: str) -> str:
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name=MODEL,
        temperature=0,
        reasoning_effort="low",
    )

    @tool("get_stock_data")
    def stock_tool(ticker: str) -> str:
        """Fetch live stock market data. Input: the stock ticker symbol, e.g. AAPL, MSFT, UBS.
        Returns price, market cap, PE ratio, 52-week high/low, volume."""
        return get_stock_data(ticker)

    @tool("search_news")
    def news_tool(query: str) -> str:
        """Search for the latest news about a company. Input: a search query,
        e.g. 'Apple Inc earnings 2026'. Returns recent news articles."""
        return search_news(query)

    @tool("search_document")
    def document_tool(question: str) -> str:
        """Search the uploaded annual report or 10-K PDF. Input: a question,
        e.g. 'What are the main risk factors?'. Returns relevant passages."""
        return search_document(question)

    tools = [stock_tool, news_tool, document_tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are FinLens AI, an elite financial research analyst.
Use the tools to gather live market data, recent news, and document insights, then write the brief.
Every number must come from a tool call, never from memory.
You MUST call all three tools (get_stock_data, search_news, search_document) at least once.
If no document is loaded, search_document will tell you so; only then say no document was provided.
Base the Key Risks section only on the news and document findings, not on general assumptions.

Your final answer MUST use this structure:

═══════════════════════════════════════════════
FINSIGHT RESEARCH BRIEF — {company_name} ({ticker})
═══════════════════════════════════════════════

📊 COMPANY OVERVIEW
[2-3 sentences about what the company does]

📈 LIVE MARKET DATA
Present the data as individual labeled lines, one metric per line, like this:
Price:          $XXX.XX
Market Cap:     $X.XXT
PE Ratio:       XX.X
52-Week High:   $XXX.XX
52-Week Low:    $XXX.XX
Volume:         XXM shares
Dividend Yield: X.XX%
Sector:         XXXXX
Do NOT write this as a paragraph. Each metric on its own line.

📰 LATEST NEWS & SENTIMENT
[Top news summary — end with Overall Sentiment: POSITIVE/NEUTRAL/NEGATIVE]

📄 KEY INSIGHTS FROM DOCUMENT
[Insights from uploaded PDF. If none uploaded, state that.]

⚠️ KEY RISKS
[3-5 bullet points]

🔮 OUTLOOK
[2-3 sentences on outlook]"""),
        ("human", "Research {company_name} ({ticker}) and generate the complete research brief."),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
    )

    result = executor.invoke({
        "company_name": company_name,
        "ticker": ticker,
    })

    return result.get("output", "Could not generate research brief.")