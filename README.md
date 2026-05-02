# Binance Futures Testnet Trading Bot

## Overview

A modular and production-ready Python CLI application that places MARKET and LIMIT orders on Binance Futures Testnet (USDT-M). Built with clean architecture, validation, logging, and structured output.

## Features

- Place MARKET and LIMIT orders
- Supports BUY and SELL
- CLI interface using Typer
- Input validation (fail-fast)
- Structured logging (bot.log)
- Clean output formatting
- Modular architecture (client, orders, validators)

## Project Structure

```
trading_bot/
├── bot/
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   ├── models.py
│   ├── exceptions.py
│   ├── logging_config.py
├── cli.py
├── .env.example
├── requirements.txt
├── README.md
├── journal.md
```

## Setup Instructions

1. Clone the repository

```bash
git clone <your-repo-url>
cd trading_bot
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Setup environment variables

Create a `.env` file:

```env
API_KEY=your_api_key
API_SECRET=your_api_secret
```

4. Get Binance Testnet API Keys

- Go to: https://testnet.binancefuture.com
- Create API key
- Enable Futures trading

## Usage

### MARKET Order

```bash
python cli.py BTCUSDT BUY MARKET 0.01
```

### LIMIT Order

```bash
python cli.py BTCUSDT SELL LIMIT 0.01 60000
```

## Example Output

```
---
## Order Summary

Symbol      : BTCUSDT
Side        : BUY
Type        : MARKET
Quantity    : 0.01

---

## Result

Order ID    : 13099696425
Status      : NEW
Executed Qty: 0.0
Avg Price   : 0.0
```

## Logging

All API activity is logged to `bot.log` in the repository root.

Example:

```
2026-05-02 17:59:01 - INFO - Placing MARKET order BTCUSDT BUY 0.01
2026-05-02 17:59:02 - INFO - Order Success ID=13099696425 Status=NEW
```

## Error Handling

- Validation errors handled before API call
- API errors wrapped and displayed cleanly

Example:

```
---
❌ Error

Message: Invalid side: must be BUY or SELL
```

## Design Principles

- Separation of concerns
- Clean architecture
- Fail-fast validation
- Structured logging
- Reusable components

## Assumptions

- Using Binance Futures Testnet (not mainnet)
- MARKET orders may return status NEW on testnet
- LIMIT orders must follow exchange price constraints

## Testing

- Tested with real Binance Futures Testnet API
- MARKET and LIMIT orders verified

## Requirements

- Python 3.x
- python-binance
- python-dotenv
- typer

## Future Improvements

- Stop-Limit / advanced order types
- Multi-command CLI
- UI dashboard

## Author

Aradhya Tiwari

## Journal

Development progress is tracked in `journal.md`.
