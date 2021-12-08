# Bookmarker

Bookmarker is a simple bookmark manager. It is meant to be similar to the bookmarker manager [Saved.io](https://saved.io/). Users can save a URL by prepending it with the hostname of the server that Bookmarker is deployed on. Therefore, to bookmark [Google](https://www.google.com), the user would go to the following URL:

```
<hostname/domain name>/https://www.google.com/
```

The frontend of this web application uses Vue.js and Bootstrap. The backend uses Django.

## Requirements and Installation

To set up Bookmarker, the following need to be installed:

- Python 3.9.
- A Postgres server.
- An SMTP server for sending email confirmations.
- Node 14 and npm 16+ to generate the static files. Not needed once static files are generated.

The web app requires multiple environment values to be set before it can be deployed. The following can be set using either environment variables or a .env file present in the repository root:

- DEBUG (Default is False.)
- DJANGO_SECRET_KEY (Secret key for Django.)
- ALLOWED_HOST (Value for Django's [ALLOWED_HOSTS](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts) setting. Optional if DEBUG is True.)
- DB_HOST (Hostname of Postgres server.)
- DB_PORT (Port of Postgres server.)
- DB_USER (Postgres user.)
- DB_PASSWORD (Postgres password.)
- DB_NAME (Postgres database name.)

If DEBUG is True, then Bookmarker will use [Django's console backend](https://docs.djangoproject.com/en/3.2/topics/email/#console-backend) for outputting email confirmations. Because of this, a real SMTP server is not needed during development. If DEBUG is False, then the following environment values should also be set:

- EMAIL_HOST (Hostname of SMTP server.)
- EMAIL_PORT (Port of SMTP server. Default is 25)
- EMAIL_HOST_USER (User of SMTP server. Default is anonymous.)
- EMAIL_HOST_PASSWORD (Password of SMTP server. Default is blank.)
- EMAIL_USE_TLS (Use TLS when connecting to to SMTP server. Default is False.)
- EMAIL_USE_SSL (Use SSL when connecting to to SMTP server. Default is False.)

After the environment variables have been set, run the following commands (preferably in a Python virtual environment) to install the required packages, generate the necessary static files, and perform database migrations:

```
pip install -r requirements.txt
npm install
npm run build
python manage.py migrate
```

## Development Server

After installing the requirements and running the necessary commands, run this command to start the Django development server:

```
python manage.py runserver
```

## Docker

Bookmarker is available as a [Docker image](https://hub.docker.com/r/onstop4/bookmarker). Running the development server inside a Docker container requires the necessary environment variables to be passed.

For local development, Docker Compose can be used to easily start Bookmarker along with a Postgres server and a simple SMTP server. If database migrations need to be performed, you can run the `migrate` script to start the Postgres server and perform the migrations. Otherwise, just run `docker-compose up` to start Bookmarker.

## Deploying

The WSGI application callable is located in `project/wsgi.py`. To deploy, follow the instructions in the "Requirements" section above and then provide your WSGI server with the path to the application callable.

For example, to deploy Bookmarker using Gunicorn using its default settings, run the following command (with the required environment variables set):

```
gunicorn project.wsgi
```

See the [Django documentation](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/) for more details on how to deploy Django applications. Please note that if your deployment of Bookmarker involves multiple hostnames, you will need to modify the ALLOWED_HOSTS list inside `project/settings.py`.

## Contributing

Before making any changes, please install the development dependencies and pre-commit hooks by running the commands below:

```
pip install -r requirements-dev.txt
pre-commit install
```

The pre-commit hooks (Black and Prettier) help to ensure that the style of the code is consistent.
