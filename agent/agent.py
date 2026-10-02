import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import Tool
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

    tools = [
        Tool(
            name="get_stock_data",
            func=get_stock_data,
            description=(
                "Fetches live stock market data. "
                "Input must be the stock ticker symbol e.g. AAPL, MSFT, UBS. "
                "Returns price, market cap, PE ratio, 52-week high/low, volume."
            ),
        ),
        Tool(
            name="search_news",
            func=search_news,
            description=(
                "Searches for latest news about a company. "
                "Input should be a search query like 'Apple Inc earnings 2026'. "
                "Returns recent news articles."
            ),
        ),
        Tool(
            name="search_document",
            func=search_document,
            description=(
                "Searches the uploaded annual report or 10-K PDF. "
                "Input should be a question like 'What are the main risk factors?'. "
                "Returns relevant passages from the document."
            ),
        ),
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are FinLens AI, an elite financial research analyst.
Use the tools to gather live market data, recent news, and document insights, then write the brief.
Every number must come from a tool call, never from memory.

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