pretix LDAP
==========================

LDAP authentication plugin for `pretix`_.

Installation
------------

You can install the plugin using ::

  $ pip install pretix-ldap

You need to enable the plugin by including ``pretix_ldap.LDAPAuthBackend`` in the ``auth_backends`` option in your ``pretix.cfg`` (see https://docs.pretix.eu/en/latest/admin/config.html).

You also need to add a ``[ldap]`` section in your ``pretix.cfg`` to configure the connection to the ldap server.

Options are:

``bind_url``
    The url of the ldap server (required)

``bind_dn``
    The dn of the account to use to query the ldap server (required)

``bind_password``
    The password of the account to use to query the ldap server (required)

``search_base``
    The search base (required)

``search_filter``
    Filter to search for users. You can use placeholders in curly braces, which will get populated from form fields of the same name.
    Default: ``(&(objectClass=inetOrgPerson)(mail={email}))``

``email_attr``
    The name of an attribute that can be used to retrieve the user's email address
    Default: ``mail``

``unique_attr``
    The name of a stable attribute that can be used to uniquely identify a user
    Default: ``dn``
    Example: ``entryUUID``

Example Deployment
------------------

An example deployment using ``docker-compose`` can be found in the ``example`` folder.

After running ``docker-compose up`` you should be able to log in at ``http://localhost:80/control`` using the email "admin@example.com" and password "password".


Development setup
-----------------

1. Make sure that you have a working `pretix development setup`_.

2. Clone this repository, eg to ``local/pretix-ldap``.

3. Activate the virtual environment you use for pretix development.

4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.

5. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.


License
-------


Copyright 2019 sohalt

Released under the terms of the Apache License 2.0



.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
