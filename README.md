# VictimsAdvocate – End-to-End Tests

Playwright + Pytest suite that exercises the public site and admin portal of the
[VictimsAdvocate](../VictimsAdvocate) project.

## What's covered

- **Public UI** (`tests/test_public_site_ui.py`)
  - Page loads, title, branding
  - Skip-to-content link, `<main>` landmark, search ARIA
  - Navigation between Home / Resources / Contact
  - Search filters
  - Share modal opens, has 3 tabs, email field accepts input
  - Multi-select cap (5 max)
- **Admin UI** (`tests/test_admin_ui.py`)
  - Login
  - Add a banner (brochure)
  - Remove a banner
  - Form validation
- **API** (`tests/test_api.py`)
  - Supabase REST: categories + brochures load
  - Brochure row shape
  - RLS: anon insert is rejected
  - `phone_number` / `business_hours` columns exist

> Email **delivery** is intentionally not tested (no real send). The email
> *text/UI* feature is covered by `test_share_modal_email_input_accepts_text`.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate                  # Windows
pip install -r requirements.txt
playwright install chromium

cp .env.test.example .env.test          # then fill in real values
```

`.env.test` keys:

| Key                   | Used by   | Notes                                              |
| --------------------- | --------- | -------------------------------------------------- |
| `BASE_URL`            | UI tests  | Defaults to `http://localhost:5173`                |
| `SUPABASE_URL`        | API tests | From the main project's `.env`                     |
| `SUPABASE_ANON_KEY`   | API tests | From the main project's `.env`                     |
| `ADMIN_EMAIL`         | Admin UI  | A user that exists in Supabase Auth                |
| `ADMIN_PASSWORD`      | Admin UI  | …with admin privileges                             |

## Running

Start the app first (in another terminal, from the main project):

```bash
cd ../VictimsAdvocate
npm run dev
```

Then run tests:

```bash
pytest                           # all tests
pytest -m smoke                  # quick smoke tests only
pytest -m ui                     # UI only
pytest -m api                    # API only
pytest -m "ui and admin"         # admin UI only
pytest --headed                  # watch the browser
pytest --headed --slowmo 500     # slow-motion debugging
```

## Layout

```
.
├── conftest.py              fixtures (base_url, admin_page, supabase creds)
├── pages/                   Page Object pattern
│   ├── public_page.py
│   └── admin_page.py
├── tests/
│   ├── test_public_site_ui.py
│   ├── test_admin_ui.py
│   └── test_api.py
├── pytest.ini
├── requirements.txt
└── .env.test.example
```

## Notes

- The admin route is `/admin` (path-based, see `src/lib/helpers.js` in the app).
- Delete uses a native `window.confirm`; the page object auto-accepts via
  `page.once("dialog", ...)`.
- Tests run against whatever `BASE_URL` points to. If you run them against
  prod, the add/remove tests will create and delete real records.
