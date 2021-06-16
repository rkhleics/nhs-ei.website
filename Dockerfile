# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster as app

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=cms.settings.base \
    PORT=8000



# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
    python-dev \
 && rm -rf /var/lib/apt/lists/*

# Install nodejs LTS
RUN curl -sL https://deb.nodesource.com/setup_lts.x | bash -
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    nodejs \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.importer.txt /
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Install node packages
ENV NPM_CONFIG_CACHE=/tmp/.npm
RUN npm install
RUN npm run build

# Collect static files.
RUN python manage.py collectstatic --noinput --clear
ENTRYPOINT ["./entrypoint.sh"]

CMD gunicorn --access-logfile - cms.wsgi:application
