# matrix-registration (maintained fork)

A simple Python application enabling token-based registration for Matrix servers.

You may have encountered the situation where you want to invite people to create
an account on your homeserver, but neither want to open up public registration
nor create every account yourself. With matrix-registration you generate tokens
on the fly and share them, letting invitees register themselves.

## About this fork

This is a maintained fork of [zeratax/matrix-registration](https://github.com/zeratax/matrix-registration),
which was archived (read-only) in 2025 with its last tagged release (v0.9.1) in
2021.

It exists for two reasons:

1. **The delete-token API.** Upstream merged a token-management API that adds
   `PATCH`/`DELETE` on `/api/token/<token>` (from pull request #87), but that work
   was never cut as a release, so it only ever existed on an untagged commit. This
   fork carries it as a proper, tagged release.
2. **Modernization.** The original froze on Python 3.7-3.9 and 2021-era libraries
   (Flask 1.x/2.x, SQLAlchemy 1.x, Flask-Limiter 1.x) via a legacy
   `setup.py install`. This fork is ported to current, non-deprecated libraries
   (Flask 3, SQLAlchemy 2.0, Flask-SQLAlchemy 3, Flask-Limiter 3, WTForms 3) and
   packaged with `pyproject.toml`, so it builds and runs on current Python
   (3.11-3.14).

Behavior and the HTTP API are unchanged from the upstream delete-token commit; the
port is limited to framework-API updates (the Flask-Limiter constructor signature,
the Flask CLI wiring, and the SQLAlchemy 2.0 session/query forms). The
self-service registration page and its translations are preserved.

Full credit for the original application goes to Jona Abdinghoff (ZerataX) and the
upstream contributors.

## Setup

Install from a checkout:

```bash
pip install .
```

### First start

Run `matrix-registration serve`. A configuration file is generated on first start
if one is not found. Copy [config.sample.yaml](/config.sample.yaml) to `config.yaml`,
edit it, and pass `--config-path /path/to/config.yaml` if it is not auto-discovered.

For `server_location`, a local connection such as `localhost:8008` (whatever port
Synapse listens on) is recommended. Connecting over the internet works too, but
you must make `/_synapse/admin/v1/register` reachable.

## Usage

```
$ matrix-registration -h
Usage: matrix-registration [OPTIONS] COMMAND [ARGS]...

  a token based matrix registration app

Options:
  --config-path TEXT  specifies the config file to be used
  -h, --help          Show this message and exit.

Commands:
  generate  generate new token
  serve     start api server
  status    view status or disable
```

Once the API server is running and a token is generated, register an account
either with a POST request:

```bash
curl -X POST \
     -F 'username=test' \
     -F 'password=verysecure' \
     -F 'confirm=verysecure' \
     -F 'token=DoubleWizardSki' \
     http://localhost:5000/register
```

or by visiting `http://localhost:5000/register?token=DoubleWizardSki`.

### Token management API

Authenticate with `Authorization: SharedSecret <admin_api_shared_secret>`.

- `POST /api/token` , create a token (JSON body: `max_usage`, `expiration_date`).
- `GET /api/token` , list tokens.
- `GET /api/token/<token>` , show one token.
- `PATCH /api/token/<token>` , update a token (e.g. `{"disabled": true}`).
- `DELETE /api/token/<token>` , delete a token. *(the delete-token API)*

## Reverse proxy

Example nginx snippet to run behind a reverse proxy:

```nginx
location ~ ^/(static|register) {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://localhost:5000;
}
```

The web API endpoints (`/api/token...`) need forwarding too if you use them.

## Translations

The registration page auto-selects a language from the browser (`?lang=` /
`Accept-Language`) and falls back to English. Translation catalogs live in
[matrix_registration/translations](/matrix_registration/translations) as
`messages.<lang>.yaml`; add a language by adding a catalog with the same keys.

## Artwork attribution

- The valley cover photo on the registration page is a photo by
  [Jesus Roncero](https://www.flickr.com/golan), used under
  [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). No warranties
  are given.
- The registration page font is [Nunito](https://fonts.google.com/specimen/Nunito),
  licensed under the
  [SIL Open Font License 1.1](./matrix_registration/static/fonts/NUNITO-LICENSE).

## License

MIT, unchanged from upstream. See [LICENSE](/LICENSE) (Copyright (c) 2018 Jona
Abdinghoff and contributors).
