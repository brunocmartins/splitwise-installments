# Splitwise Installment Manager

A Python project to manage and automate installment-based expenses in [Splitwise](https://www.splitwise.com/), featuring both a command-line interface (CLI) and a web application.

## Features

- **Add installment expenses** to a Splitwise group, split equally among members.
- **List available categories and subcategories** from Splitwise.
- **Web interface** for easy entry of installment expenses.
- **CLI** for power users and automation.

## Requirements

- Python 3.10+
- [Splitwise Python SDK](https://github.com/namaggarwal/splitwise)
- Flask
- Click
- python-dotenv
- requests

## Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:brunocmartins/splitwise-installments.git
   cd splitwise-installments
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -r pyproject.toml
   ```
   This project uses [uv](https://github.com/astral-sh/uv) for fast and reproducible dependency management. All dependencies are specified in `pyproject.toml` and locked in `uv.lock`.

   If you need to install the Splitwise SDK directly:
   ```bash
   uv pip install splitwise
   ```

## Configuration

Create a `.env` file in the project root with your Splitwise API credentials:

```env
API_KEY=your_splitwise_api_key
CONSUMER_KEY=your_splitwise_consumer_key
CONSUMER_SECRET=your_splitwise_consumer_secret
FLASK_SECRET_KEY=your_flask_secret_key
```

- You can obtain your Splitwise API credentials by registering an app at [Splitwise Developers](https://dev.splitwise.com/).
- The `FLASK_SECRET_KEY` is required for session security in the web app.

## Usage

### Command-Line Interface (CLI)

Run the CLI from the project root:

```bash
python -m src.cli [COMMAND] [OPTIONS]
```

#### Commands

- **Add an installment expense:**
  ```bash
  python -m src.cli add \
    --amount 120.00 \
    --installments 3 \
    --description "Gym Membership" \
    --date 2024-07-01 \
    --group-id 12345678 \
    --category "Personal" \
    --subcategory "Health"
  ```

- **List categories:**
  ```bash
  python -m src.cli list-categories
  ```

  To list subcategories for a specific category:
  ```bash
  python -m src.cli list-categories --category "Personal"
  ```

### Web Application

1. **Start the web server:**
   ```bash
   python src/webapp.py
   ```

2. **Open your browser and go to:**
   ```
   http://127.0.0.1:5000/
   ```

3. **Fill out the form** to add an installment expense.

## Environment Variables

- `API_KEY`: Splitwise API key (optional, for API key auth)
- `CONSUMER_KEY`: Splitwise consumer key (required)
- `CONSUMER_SECRET`: Splitwise consumer secret (required)
- `FLASK_SECRET_KEY`: Flask secret key (required for web app)
- `GROUP_ID`: (optional) Default Splitwise group ID

## Project Structure

```
splitwise/
  src/
    cli.py           # CLI entry point
    installment.py   # Business logic for installments
    webapp.py        # Flask web application
    templates/
      index.html     # Web UI template
  pyproject.toml     # Project metadata and dependencies
  uv.lock            # Lock file for uv/pip
  README.md          # This file
```

## Development

- Code style: [PEP8](https://www.python.org/dev/peps/pep-0008/)
- PRs and issues are welcome!

## License

MIT License

---

**Note:** This project is not affiliated with or endorsed by Splitwise. Use at your own risk.
