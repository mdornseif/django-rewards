django-rewards
==============

Django rewards is a reusable application for Affiliate Marketing (inbound, you are the one who is paying the aliliates money) Capmaign tracking and other pay per preformance marketing approaches.

It is in early development, although parts of it have been in use since a few years.

Currently it only supports Campaign tracking.

Usage
-----

The dependencies for django-rewards can be found in the file requirements.txt. If you have pip_ installed,
you can install all dependencies with the following command::

    pip install -r requirements.txt

.. _pip: http://pypi.python.org/pypi/pip


Then you have to configure your Django Project. Add ``'rewards.middleware.RewardsMiddleware',`` *after* the
line that reads ``'django.contrib.sessions.middleware.SessionMiddleware',`` in the ``MIDDLEWARE_CLASSES``
section of your ``settings.py`` file. Also add ``'rewards',`` in the ``INSTALLED_APPS`` section. Your
``settings.py`` should have now the following settings (besides other stuff)::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'rewards.middleware.RewardsMiddleware',
    )
    
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',
        'rewards',
    )


Finally create the needed Database Tables::

    python manage.py syncdb rewards

