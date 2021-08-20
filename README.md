# Bookmarker

Bookmarker is a simple bookmark manager. It is meant to be similar to the bookmarker manager [Saved.io](https://saved.io/). Users can save a URL by prepending it with the hostname of the server that Bookmarker is deployed on. Therefore, to bookmark [Google](https://www.google.com), the user would go to the following URL:

```
<hostname>/https://www.google.com/
```

The frontend of this web application uses Vue.js and Bootstrap. The backend uses Django.

## Requirements

- A WSGI server to run the web app. Python 3.9 must be installed.
- A Postgres server.
- An SMTP server for sending email confirmations.
- A web server that can serve the static files stored in the `static_collected` directory (see below).
- npm to generate the static files.

The Python requirements for the web app can be installed by running `pip install -r requirements.txt` (preferably in a virtual environment). The static files can be generated and consolidated by running the following commands:

```
npm install
npm run build
python manage.py collectstatic
```

The last command will consolidate all of the static files into a directory in the repository root called `static_collected`.

The web app requires several values to be set before it can be deployed. The following can be set using either environment variables or a .env file present in the repository root:

- DEBUG (default is False)
- DJANGO_SECRET_KEY
- DB_HOST
- DB_PORT
- DB_USER
- DB_PASSWORD
- DB_NAME
- EMAIL_HOST (default is localhost)
- EMAIL_PORT (default is 25)
- EMAIL_HOST_USER (default is anonymous)
- EMAIL_HOST_PASSWORD (default is blank)
- EMAIL_USE_TLS (default is False)
- EMAIL_USE_SSL (default is False)

## Development and Contributing

Before making any changes, please install the development dependencies and pre-commit hooks by running the commands below:

```
pip install -r requirements-dev.txt
pre-commit install
```

The pre-commit hooks (Black and Prettier) help to ensure that the style of the code is consistent.
