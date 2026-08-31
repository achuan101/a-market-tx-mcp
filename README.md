# A-Market MCP

A stock market data MCP server using Tencent and Sina APIs.

## 依赖安装

```bash
pip install mcp requests
```

## MCP 配置

在 Qoder IDE 的 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "a-market-mcp": {
      "command": "python",
      "args": ["<项目绝对路径>\\server.py"]
    }
  }
}
```


## 工具列表

| 工具 | 说明 |
|------|------|
| `tencent_kline` | 查询历史 K 线数据 |
| `tencent_quote` | 查询实时行情快照 |
| `sina_stock_search` | 按关键词搜索股票代码 |
