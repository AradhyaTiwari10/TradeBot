# Project Journal

- 2026-05-02T15:47:02.163+05:30 - Project initialized. Folder structure created: trading_bot/ with bot/ subpackage and placeholders for client, orders, validators, models, exceptions, logging.
- Tech stack chosen: python-binance, python-dotenv, typer.
- Notes: No logic implemented. This is an architectural skeleton ready for incremental development.

TODO:
- Record design decisions and milestones as development progresses.


Timestamp: 2026-05-02T16:03:13.146+05:30

Milestone: Client Layer

Changes:

* Implemented Binance client initialization
* Loaded environment variables using dotenv
* Added validation for API keys

Files Modified:

* bot/client.py

Notes:

* Assumes python-binance supports `testnet=True` and that python-dotenv is installed. The function raises ValueError if credentials are missing and does not print or exit.


Timestamp: 2026-05-02T16:15:32.145+05:30

Milestone: Models + Exceptions

Changes:

* Created OrderRequest and OrderResponse dataclasses
* Added custom exceptions: ValidationError, APIError

Files Modified:

* bot/models.py
* bot/exceptions.py

Notes:

* Dataclasses chosen for lightweight, serializable structures without runtime validation; keeps models decoupled from business logic.
