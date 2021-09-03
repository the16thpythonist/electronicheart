
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Required library for argon python package
  && apt-get install -y libffi-dev \
  # Required libraries for pillow python package
  && apt-get install -y libjpeg-dev zlib1g-dev libfreetype6-dev libopenjp2-7 libtiff5 \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY --chown=django:django ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
COPY --chown=django:django . /app

# Need to install a language model for the profanity filter
# https://stackoverflow.com/questions/53911615/not-able-to-load-english-language-module-of-spacy-with-spacy-loaden
RUN python -m spacy download en

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
