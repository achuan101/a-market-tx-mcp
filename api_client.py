import requests
import json
import logging

logger = logging.getLogger("a_market_mcp")
logger.setLevel(logging.INFO)

def get_tencent_kline(symbol: str, period: str = "day", count: int = 260, adjust: str = "qfq") -> dict:
    url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={symbol},{period},,,{count},{adjust}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        if data.get("code") != 0:
            return {"error": f"Tencent API error: {data.get('msg')}"}
            
        stock_data = data.get("data", {}).get(symbol)
        if not stock_data:
            return {"error": f"No data found for symbol {symbol}"}
            
        # Determine the correct key for the K-line data
        kline_key = f"{adjust}{period}" if adjust else period
        if kline_key not in stock_data:
            # Fallback to just period (like 'day')
            kline_key = period
            
        klines = stock_data.get(kline_key, [])
        
        # Clean up data (take only first 6 columns: date, open, close, high, low, volume)
        cleaned_klines = [row[:6] for row in klines]
        
        return {
            "symbol": symbol,
            "period": period,
            "adjust": adjust,
            "klines": cleaned_klines
        }
    except Exception as e:
        return {"error": str(e)}

def get_tencent_quote(symbols: list) -> dict:
    symbols_str = ",".join(symbols)
    url = f"http://qt.gtimg.cn/q={symbols_str}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        r.encoding = 'gbk'
        
        results = {}
        lines = r.text.strip().split('\n')
        for line in lines:
            if not line:
                continue
            # Example: v_sz002463="51~沪电股份~002463~96.55...
            parts = line.split('=')
            if len(parts) != 2:
                continue
            key_part = parts[0]
            val_part = parts[1].strip('";')
            
            # Extract symbol from v_sz002463
            symbol = key_part.split('_')[1] if '_' in key_part else key_part
            
            fields = val_part.split('~')
            if len(fields) > 30:
                results[symbol] = {
                    "name": fields[1],
                    "code": fields[2],
                    "current_price": fields[3],
                    "prev_close": fields[4],
                    "open": fields[5],
                    "volume": fields[6],
                    "turnover": fields[37] if len(fields)>37 else None,
                    "market_cap": fields[45] if len(fields)>45 else None,
                    "pe_ratio": fields[39] if len(fields)>39 else None
                }
        return {"quotes": results}
    except Exception as e:
        return {"error": str(e)}

def search_sina_stock(keyword: str) -> dict:
    url = f"http://suggest3.sinajs.cn/suggest/type=&key={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        r.encoding = 'gbk'
        
        # Example: var suggestvalue="002463,sz002463,沪电股份...";
        text = r.text.strip()
        prefix = 'var suggestvalue="'
        if text.startswith(prefix):
            content = text[len(prefix):-2] # remove var suggestvalue=" and ";
            
            results = []
            if content:
                items = content.split(';')
                for item in items:
                    fields = item.split(',')
                    if len(fields) >= 4:
                        # Sina suggest format: name, type, code, symbol, name2, ...
                        # e.g., 沪电股份,11,002463,sz002463,沪电股份
                        name = fields[0]
                        symbol = fields[3]
                        results.append({"name": name, "symbol": symbol})
            return {"keyword": keyword, "results": results}
        else:
            return {"error": "Invalid format returned from Sina API"}
            
    except Exception as e:
        return {"error": str(e)}
