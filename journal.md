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


Timestamp: 2026-05-02T17:15:49.722+05:30

Milestone: CLI Layer

Changes:

* Implemented CLI using Typer
* Integrated order placement flow
* Added structured output formatting

Files Modified:

* cli.py

Notes:

* CLI improves developer ergonomics by providing a single command to place testnet orders; it only orchestrates existing components and does not perform validation.


Timestamp: 2026-05-02T17:20:00.000+05:30

Milestone: CLI Fix

Changes:

* Use typer.Argument for positional arguments to avoid parsing ambiguity for optional price

Files Modified:

* cli.py

Notes:

* This change makes the positional 'price' argument unambiguous and prevents Typer from treating earlier tokens as the quantity.


Timestamp: 2026-05-02T17:27:04.250+05:30

Milestone: Validation Layer

Changes:

* Implemented input validation for OrderRequest: side, order_type, quantity, price
* Integrated validate_order_request into place_order before API calls

Files Modified:

* bot/validators.py
* bot/orders.py

Notes:

* Validation is kept separate from business logic and raises ValidationError on invalid inputs. Quantity and price must be positive numbers; side and order_type are constrained to BUY/SELL and MARKET/LIMIT respectively.


Timestamp: 2026-05-02T17:30:58.105+05:30

Milestone: Validation Layer (CLI Integration)

Changes:

* Added public function validate_order(order: OrderRequest)
* Integrated validation into CLI before API call

Files Modified:

* bot/validators.py
* cli.py

Notes:

* validate_order is an alias to the internal validate_order_request to provide the exact API requested. Validation prevents invalid API calls and improves reliability.


Timestamp: 2026-05-02T17:32:32.042+05:30

Milestone: Logging System

Changes:

* Implemented centralized logging configuration
* Added request and response logging in order execution
* Integrated logging into CLI startup

Files Modified:

* bot/logging_config.py
* bot/orders.py
* cli.py

Notes:

* Logging improves observability and debugging capability


Timestamp: 2026-05-02T18:03:09.072+05:30

Milestone: Logging polish

Changes:

* Improved log messages to omit price for MARKET orders and display price for LIMIT orders (e.g., "Placing LIMIT order BTCUSDT SELL 0.01 @ 60000").

Files Modified:

* bot/orders.py

Notes:

* This keeps logs concise and avoids showing 'None' for MARKET orders.


Timestamp: 2026-05-02T18:06:21.008+05:30

Milestone: Output Formatting

Changes:

* Improved CLI output formatting for readability
* Added structured sections for summary and result
* Standardized error output

Files Modified:

* cli.py

Notes:

* Output is aligned and professional for evaluators and users.


Timestamp: 2026-05-02T18:03:09.072+05:30

Milestone: Logging polish

Changes:

* Improved log messages to omit price for MARKET orders and display price for LIMIT orders (e.g., "Placing LIMIT order BTCUSDT SELL 0.01 @ 60000").

Files Modified:

* bot/orders.py

Notes:

* This keeps logs concise and avoids showing 'None' for MARKET orders.
