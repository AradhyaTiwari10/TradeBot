# Binance Futures Testnet Trading Bot

## Overview

A compact, production-oriented Python CLI that places MARKET, LIMIT and STOP_LIMIT orders on Binance Futures Testnet (USDT-M). Focused on fast setup, safety (validation), and clear CLI output.

## ⚙️ Features

- MARKET, LIMIT, and STOP-LIMIT orders
- BUY and SELL support
- CLI with multi-command interface (trade, info)
- Input validation (fail-fast)
- Exchange-aware validation (minQty, stepSize, tickSize, minPrice)
- Structured logging (bot.log)
- Clean, readable output
- Modular architecture

## Project structure

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

## Setup

1. Clone the repository

```bash
git clone <your-repo-url>
cd trading_bot
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env` with testnet keys

```env
API_KEY=your_api_key
API_SECRET=your_api_secret
```

4. Get Binance Futures Testnet API keys: https://testnet.binancefuture.com

## ▶️ Usage

### Trade (MARKET)

```bash
python cli.py trade BTCUSDT BUY MARKET 0.01
```

Trade (LIMIT)

```bash
python cli.py trade BTCUSDT SELL LIMIT 0.01 60000
```

Trade (STOP-LIMIT)

```bash
python cli.py trade BTCUSDT BUY STOP_LIMIT 0.01 72000 71000
```

Symbol Info (exchange rules)

```bash
python cli.py info BTCUSDT
```

---

## 📊 Example Output

### info command

```
Symbol: BTCUSDT
minQty : 0.001
stepSize: 0.001
tickSize: 0.1
minPrice: 0.1
```

## Validation & assumptions

- Inputs are validated locally; exchange rules (when available) are enforced before API calls.
- STOP-LIMIT orders must respect trigger rules relative to market price (else Binance returns error -2021).

## 🧪 Testing

- Verified MARKET, LIMIT, and STOP-LIMIT orders on Binance Futures Testnet
- Verified exchange-aware validation prevents invalid orders before API calls

## Logging

Actions and responses are logged to `bot.log` (INFO). Logs never include API keys.

## Requirements

- Python 3.8+
- python-binance
- python-dotenv
- typer

## Security

Do not commit `.env` or `bot.log`. If they were committed, remove from history and rotate keys.

## Author

Aradhya Tiwari

## Journal

Development progress is tracked in `journal.md`.
