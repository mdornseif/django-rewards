django-rewards
==============

Django rewards is a reusable application for Affiliate Marketing
(inbound, you are the one who is paying the aliliates money) Capmaign
tracking and other pay per preformance marketing approaches.

It is in early development, although parts of it have been in use since
a few years.

Currently it only supports Campaign and Conversion tracking.

Usage
-----

The dependencies for django-rewards can be found in the file
requirements.txt. If you have pip_ installed, you can install all
dependencies with the following command::

    pip install -r requirements.txt

.. _pip: http://pypi.python.org/pypi/pip


Then you have to configure your Django Project. Add
``'rewards.middleware.RewardsMiddleware',`` *after* the line that reads
``'django.contrib.sessions.middleware.SessionMiddleware',`` in the
``MIDDLEWARE_CLASSES`` section of your ``settings.py`` file. Also add
``'rewards',`` in the ``INSTALLED_APPS`` section. Your ``settings.py``
should have now the following settings (besides other stuff)::

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


Finally create the needed database tables::

    python manage.py syncdb rewards

This should have automatically created an campaign with the ID
"dcTESTESTESTESTESTESTESTESTE". Campaigns are the categories in which
you do tracking. Every affiliate is associated (one to one) with an
campain but you can also use campains to track other things, e.g.
movements of visitors between your different Web properties or
effectiveness of advertising.

Tracking is done by appending ``?aff=<campagin id>`` to the URL. This
will fill ``request.session['campaign']`` of the current sessions with
the campain id. It also will register the visit as an "inflow" in the
Database.

To register "conversions" ("goals": sales, subscriptions, whatever) you
need to call ``rewards.regcon_by_request()`` at the location where the
actual Conversion happens. Usualy that is the checkout of your Shop, or
the sign-up form of your Newsletter, or whatever.

The most important parameter to ``regcon_by_request()`` is the *value*,
This is an integer number representing the value of the goal. For a
newsletter subscription it might be always "1". For a Shopping Cart you
probably want to use the cart's monetary value.

Keep in Mind, that you can only use Integers. So if You use a float or a
Decimal() to represent prices, probably the best thing is to multiply
and use the smallest currency unit of your Country (e.g. "cent" for
Europe).

Other Parameters are ``reference`` which should be an ID for the
transaction triggering the conversion. Usually this should be the order
number or something like that and the parameter ``text`` could be a
human readable description of the transaction.

As a concrete example your checkout-view in your shop might look like
this::

    ...
    order = Order.objects.create(price=16.95, shipping=4.50, ...)
    rewards.regcon_by_request(request, order.price*100,
                              reference='order%d' % order.id,
                              text='Customer order %s' % order.id)
    return render_to_response(...)


