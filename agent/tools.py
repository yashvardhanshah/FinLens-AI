import os
import yfinance as yf
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Global vectorstore — set from app.py when PDF is uploaded
vectorstore = None

def set_vectorstore(vs):
    """Called from app.py after PDF is processed."""
    global vectorstore
    vectorstore = vs


def get_stock_data(ticker: str) -> str:
    """
    Fetches live stock data for a given ticker from Yahoo Finance.
    Returns formatted string with key financial metrics.
    """
    try:
        stock = yf.Ticker(ticker.strip().upper())
        info = stock.info

        name        = info.get("longName", "N/A")
        price       = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
        mkt_cap     = info.get("marketCap", "N/A")
        pe          = info.get("trailingPE", "N/A")
        pe = f"{pe:.1f}" if isinstance(pe, (int, float)) else pe
        week_high   = info.get("fiftyTwoWeekHigh", "N/A")
        week_low    = info.get("fiftyTwoWeekLow", "N/A")
        volume      = info.get("volume", "N/A")
        div_yield   = info.get("dividendYield", "N/A")
        sector      = info.get("sector", "N/A")
        summary     = info.get("longBusinessSummary", "N/A")[:300]

        # Format market cap
        if isinstance(mkt_cap, (int, float)):
            mkt_cap = f"${mkt_cap/1e12:.2f}T" if mkt_cap >= 1e12 else f"${mkt_cap/1e9:.2f}B"

        # Format dividend yield
        if isinstance(div_yield, float):
            div_yield = f"{div_yield:.2f}%"

        return f"""
STOCK DATA — {name} ({ticker.upper()})
Current Price:    ${price}
Market Cap:       {mkt_cap}
PE Ratio:         {pe}
52-Week High:     ${week_high}
52-Week Low:      ${week_low}
Volume:           {volume:,} shares
Dividend Yield:   {div_yield}
Sector:           {sector}
Business Summary: {summary}
        """.strip()

    except Exception as e:
        return f"Could not fetch stock data for {ticker}. Error: {str(e)}"


def search_news(query: str) -> str:
    """
    Searches the web for latest news using Tavily.
    Returns summarized news content.
    """
    try:
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        results = response.get("results", [])
        if not results:
            return "No news found for this query."

        news_text = ""
        for i, r in enumerate(results, 1):
            title   = r.get("title", "No title")
            content = r.get("content", "")[:300]
            url     = r.get("url", "")
            news_text += f"{i}. {title}\n{content}\nSource: {url}\n\n"

        return news_text.strip()

    except Exception as e:
        return f"Could not fetch news. Error: {str(e)}"


def search_document(question: str) -> str:
    """
    Searches the uploaded PDF vectorstore for relevant content.
    Returns top matching chunks as context.
    """
    if vectorstore is None:
        return "No document uploaded. Please upload an annual report or 10-K PDF."

    try:
        results = vectorstore.similarity_search(question, k=4)
        if not results:
            return "No relevant content found in the document."

        context = "\n\n".join([doc.page_content for doc in results])
        return f"DOCUMENT INSIGHTS:\n{context}"

    except Exception as e:
        return f"Could not search document. Error: {str(e)}"