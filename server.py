import json
import logging
from mcp.server.fastmcp import FastMCP
from typing import List, Optional

import api_client

logger = logging.getLogger("a_market_mcp")
logger.setLevel(logging.INFO)

mcp = FastMCP("a-market-mcp")

@mcp.tool()
def tencent_kline(symbol: str, period: str = "day", count: int = 260, adjust: str = "qfq") -> str:
    """
    Query historical K-line data (day/week/month).
    
    Args:
        symbol: Stock code (e.g. sz002463, sh600519)
        period: Period - day, week, month. Default is day.
        count: Number of k-lines to fetch. Default is 260.
        adjust: Adjust type (qfq, hfq, or empty). Default is qfq (forward adjust).
    """
    result = api_client.get_tencent_kline(symbol, period, count, adjust)
    return json.dumps(result, ensure_ascii=False)

@mcp.tool()
def tencent_minute_kline(symbol: str, period: int = 5, count: int = 240) -> str:
    """
    Query minute-level K-line data (intraday recent data).
    
    Args:
        symbol: Stock code (e.g. sz002463, sh600519)
        period: Minute interval - 1, 5, 15, 30, 60. Default is 5.
        count: Number of k-lines to fetch (max 320). Default is 240.
    """
    result = api_client.get_tencent_minute_kline(symbol, period, count)
    return json.dumps(result, ensure_ascii=False)

@mcp.tool()
def tencent_quote(symbols: List[str]) -> str:
    """
    Query real-time stock quote snapshots.
    
    Args:
        symbols: List of stock codes (e.g. ["sz002463", "sh600519"])
    """
    result = api_client.get_tencent_quote(symbols)
    return json.dumps(result, ensure_ascii=False)

@mcp.tool()
def sina_stock_search(keyword: str) -> str:
    """
    Search for stock codes by keyword (name or pinyin).
    
    Args:
        keyword: The keyword to search for (e.g. \u6caa\u7535\u80a1\u4efd or hdgf)
    """
    result = api_client.search_sina_stock(keyword)
    return json.dumps(result, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run()
