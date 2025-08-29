## Django Fund Manager

Simple Django app to import fund data from a CSV file, browse and filter funds in a web UI, and access the data via a REST API. Uses SQLite locally by default.

### Features

- Upload a CSV to create `Fund` records
- List funds in a table with a Strategy filter
- Display total fund count and total AUM
- REST API: list and detail endpoints with strategy filtering
- Automated tests via `manage.py test`

---

### Requirements

- Python 3.8+
- pip

Optional (recommended): a virtual environment

---

### Setup

1. Clone or download the repository, then open a terminal in the project root (where `manage.py` lives).

2. Create and activate a virtual environment

Windows (PowerShell):

```powershell
py -m venv venv
venv\Scripts\Activate.ps1
```

macOS/Linux (bash/zsh):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Apply database migrations

```bash
python manage.py migrate
```

5. (Optional) Create an admin user

```bash
python manage.py createsuperuser
```

6. Run the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

---

### Using the App

- Browse funds: http://127.0.0.1:8000/

  - Use the Strategy dropdown to filter
  - Bottom of the page shows total fund count and total AUM (filtered if a strategy is selected)

- Upload a CSV: http://127.0.0.1:8000/upload/
  - Upload a CSV with the following headers (exactly):
    - `Name`, `Strategy`, `AUM (USD)`, `Inception Date`
  - Sample CSV:

```csv
Name,Strategy,AUM (USD),Inception Date
Amazing Fund 1,Long/Short Equity,355000000,3/10/2011
Pretty Good Fund X,Global Macro,,4/10/2012
Quite OK Capital Fund 1,Arbitrage,256000000,10/1/2015
High Growth High Risk Fund 3,Long/Short Equity,452000000,10/1/2012
Crypto Arbitrage Strategy X,Arbitrage,123000000,6/10/2012
Another Fund Y,Global Macro,,
```

Notes:

- Empty AUM or Inception Date values are allowed.
- Dates are parsed in common formats like `MM/DD/YYYY` (e.g. `3/10/2011`).
- Files saved as UTF-8 with BOM are supported.

---

### REST API

- List funds:

```
GET /api/funds/
```

- Filter by strategy:

```
GET /api/funds/?strategy=Arbitrage
```

- Single fund detail by id:

```
GET /api/funds/1/
```

Responses are JSON. `aum` is returned as a number (or null), and `inception_date` as ISO date when present.

---

### Running Tests

```bash
python manage.py test
```

---

### Troubleshooting

- If upload fails with a header KeyError, ensure your CSV headers match exactly: `Name,Strategy,AUM (USD),Inception Date`.
- If your CSV was exported from Excel and shows odd header characters, re-save as UTF-8 (the app also accepts UTF-8 with BOM).
- If migrations fail, delete the local `db.sqlite3` (dev only) and run `python manage.py migrate` again.

---

### Production Note

This project uses SQLite for local development. For cloud deployment, use a managed PostgreSQL database and a production settings module.
