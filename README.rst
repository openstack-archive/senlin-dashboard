========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/senlin-dashboard.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

================
Senlin Dashboard
================

Senlin Management Dashboard

.. inclusion-start-marker-hosts

Project Hosting
---------------

- Documentation: https://docs.openstack.org/senlin-dashboard/latest/
- Release notes: https://docs.openstack.org/releasenotes/senlin-dashboard/
- Blueprints: https://blueprints.launchpad.net/senlin-dashboard
- Bugs: https://bugs.launchpad.net/senlin-dashboard

Mailing list
------------

Use ``[senlin-dashboard]`` prefix in subjects with for faster responses

- http://lists.openstack.org/cgi-bin/mailman/listinfo/openstack-discuss

Code Hosting
------------

- https://opendev.org/openstack/senlin-dashboard

Code Review
-----------

- https://review.opendev.org/#/q/status:open+project:openstack/senlin-dashboard,n,z

.. inclusion-end-marker-hosts

.. inclusion-start-marker-install

============
Installation
============

Before install the Senlin Dashboard, setup the Horizon.
To setup the Horizon, see
`Installation Guide
<https://docs.openstack.org/horizon/latest/install/index.html>`__
in the Horizon documentation.

1. Clone the Senlin Dashboard repository::

    $ git clone https://opendev.org/openstack/senlin-dashboard

2. Copy the ``_50_senlin.py`` file from ``senlin_dashboard/enabled/_50_senlin.py``
   file to ``horizon/openstack_dashboard/local/enabled`` directory. Example,
   set as if being executed from the root of the senlin-dashboard repository::

    cp ./senlin_dashboard/enabled/_50_senlin.py ../horizon/openstack_dashboard/local/enabled

3. Change into the senlin-dashboard repository and package the plugin::

    pip install -r requirements.txt -e .

   This will build and install the senlin-dashboard plugin into the active virtual
   environment associated with your horizon installation. The plugin is installed
   in "editable" mode as a link back to your senlin-dashboard plugin directory.

.. inclusion-end-marker-install

.. inclusion-start-marker-develop

Devstack Installation
---------------------

1. Download DevStack::

    $ git clone https://opendev.org/openstack/devstack
    $ cd devstack

2. Add following repo as external repositories into your ``local.conf`` file::

    [[local|localrc]]
    #Enable senlin
    enable_plugin senlin https://opendev.org/openstack/senlin
    #Enable senlin-dashboard
    enable_plugin senlin-dashboard https://opendev.org/openstack/senlin-dashboard

   Please see the link: https://docs.openstack.org/senlin/latest/install/index.html
   for more detail about setting Senlin Server.

3. Run ``stack.sh``::

    $ ./stack.sh

Unit Test
---------

The unit tests can be executed directly from within this Senlin Dashboard plugin
project directory by using::

    tox

.. inclusion-end-marker-develop

.. inclusion-start-marker-configuration

=============
Configuration
=============

Switch to Angularized panels
----------------------------

The panels are ongoing to migrate to AngularJS based. If you would try them,
please copy ``_59_toggle_angular_senlin_dashboard.py.example`` to
``horizon/openstack_dashboard/local_settings.d/_59_toggle_angular_senlin_dashboard.py``
and restart Horizon.

For more information on configuration, see
`Configuration Guide
<https://docs.openstack.org/horizon/latest/configuration/index.html>`__
in the Horizon documentation.

.. inclusion-end-marker-configuration

