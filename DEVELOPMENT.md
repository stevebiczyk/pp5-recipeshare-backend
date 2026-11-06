# Development and verification

Use Python 3.10–3.14 and install `requirements.txt` in a virtual environment. Django is constrained to the 5.2 series; 5.2.8 added support for Python 3.14.

From this directory in PowerShell:

```powershell
$env:DEV = '1'
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Development uses SQLite. Without Cloudinary credentials, uploaded files use the ignored `media/` directory, served by Django in development. Existing Cloudinary asset IDs in the old test database are not local files; configure Cloudinary to display those assets or replace their images through the forms. Set `CLOUDINARY_URL` to use Cloudinary uploads locally.

The old test database is retained locally but excluded from future commits. New checkouts create a database through migrations; no seed accounts are distributed. Previous Git history still contains the old test database. No history rewrite was performed.

Run tests with:

```powershell
.\venv\Scripts\python.exe manage.py test --noinput
```

`manage.py test` selects `pp5_backend_sb.test_settings` by default: in-memory database/media, fast test password hashing, and no external credentials. To select it explicitly, use `--settings=pp5_backend_sb.test_settings`. These overrides are not used by the application server.

Production requires `SECRET_KEY` and `DATABASE_URL`, with `DEV` unset or false. Configure `CLOUDINARY_URL`, the exact `CLIENT_ORIGIN` (scheme and hostname, no trailing slash), and `ALLOWED_HOST` for deployment. For frontend and API on different sites over HTTPS, set `JWT_COOKIE_SAMESITE=None`; JWT and CSRF cookies will be Secure. The default is `Lax`. Browser third-party-cookie restrictions can still require a same-site deployment. CORS and CSRF origins must match the actual frontend.

The frontend fetches a masked token from the uncached `/csrf/` endpoint before writes and sends it as `X-CSRFToken`. It does not need to read a cookie on the backend hostname. Login and registration clear its cached token before subsequent writes.

Votes expose `upvotes_count`, `downvotes_count`, and `votes_count` (net score). Existing null vote types count as legacy upvotes. The authenticated voted feed orders by `current_vote_created_at`. Profiles expose `owner_id` for follower creation; profile IDs and user IDs need not match.
