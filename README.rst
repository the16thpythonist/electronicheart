electronicheart
===============

Personal website of Jonas Teufel

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy electronicheart

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html




Vue
^^^

This app integrates with a Vue multi-page app (MPA) located in ``vue_frontend``.

To initialize the frontend, from the ``vue_frontend`` directory, run::

    $ npm install

To serve the Vue frontend in hot-reloading development mode::

    $ npm run serve

And to build for deployment::


    $ npm run serve

For more information, see ``vue_frontend/README.md``.


Deploying for production
------------------------

The following section contains the information of the individual steps needed to deploy the website to a production
server. We will assume, that the production server does not contain any relevant third party software yet. So the
instructions will also cover the installation of these dependencies. The instructions assume a debian based operating
system such as an Ubuntu server or the Raspberry Pi OS.

The first step is to fetch the project source code from this git repository.

.. code-block:: console

    sudo apt-get install git
    git clone https://github.com/the16thpythonist/electronicheart.git

**The frontend.** To setup the frontend it is first necessary to install *node.js* on the machine. For that need to
install *nvm* first.

.. code-block:: console

    sudo apt-get install curl
    curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
    source ~/.profile

Using nvm's install command will install the most recent version of node js and the node package manager *npm*.

.. code-block:: console

    nvm install
    node --version
    npm --version

We need npm to properly install the vue frontend of the application. First navigate to the corresponding frontend
folder.

.. code-block:: console

    cd electronicheart/vue_frontend
    npm install

The installation should take a few minutes. After it is done we can run the "build" script to create the compiled and
minified JS files for the frontend.

.. code-block:: console

    npm run build

With this, the frontend installation is almost done. But we still need to adjust the environmental variables to use
our hostname. For that edit the ".env" file within the frontend folder.

.. code-block:: env

    VUE_APP_STATIC_ROOT=http://{OUR HOSTNAME}/static
    VUE_APP_API_ROOT=http://{OUR HOSTNAME}/api

**The backend.** For the backend it is important to install docker first.

.. code-block:: console

    sudo apt-get install docker docker-compose

Then we need to write the appropriate "env" files. For that, first navigate to the top level folder of the project and
then start to create the necessary folder structure.

.. code-block:: console

    cd electronicheart
    mkdir .envs
    cd .envs
    mkdir .production
    cd .production
    touch .django
    touch .postgres

First open the ".postgres" file and fill it with the following content:

.. code-block:: env

    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_DB=electronicheart
    POSTGRES_USER={OUR USER}
    POSTGRES_PASSWORD={OUR PASSWORD}

Then open the ".django" file and fill it with the following env values, replacing the parts within curled brackets:

.. code-block:: env

    DJANGO_SETTINGS_MODULE=config.settings.production
    DJANGO_SECRET_KEY={VERY LONG AND RANDOM STRING}
    DJANGO_ADMIN_URL={ADMIN URL}/
    DJANGO_ALLOWED_HOSTS=.{OUR DOMAIN NAME}

    DJANGO_SECURE_SSL_REDIRECT=False
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=True

    # This controls how many concurrent worker threads you want to have
    WEB_CONCURRENCY=4

    REDIS_URL=redis://redis:6379/0

Using docker compose we can then build the necessary containers. For this navigate back to the top level folder first.

.. code-block:: console

    cd electronicheart
    sudo docker-compose -f production.yml build

Then we first need to apply all the data migrations and create a new super user.

.. code-block:: console

    sudo docker-compose -f production.yml run --rm django python manage.py migrate
    sudo docker-compose -f production.yml run --rm django python manage.py createsuperuser

