========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/senlin-dashboard.svg
    :target: http://governance.openstack.org/reference/tags/index.html

.. Change things from this point on

================
Senlin Dashboard
================

Senlin Management Dashboard

Installation
------------

1. Clone the Senlin Dashboard repository::

    $ git clone https://git.openstack.org/openstack/senlin-dashboard

2. Copy the ``_50_senlin.py`` file from ``senlin_dashboard/enabled/_50_senlin.py``
   file to ``horizon/openstack_dashboard/local/enabled`` directory. Example,
   set as if being executed from the root of the senlin-dashboard repository::

    cp ./senlin_dashboard/enabled/_50_senlin.py ../horizon/openstack_dashboard/local/enabled

3. Change into the senlin-dashboard repository and package the plugin::

    pip install -r requirements.txt -e .

   This will build and install the senlin-dashboard plugin into the active virtual
   environment associated with your horizon installation. The plugin is installed
   in "editable" mode as a link back to your senlin-dashboard plugin directory.

Devstack Installation
---------------------


1. Download DevStack::

    $ git clone https://git.openstack.org/openstack-dev/devstack
    $ cd devstack

2. Add following repo as external repositories into your ``local.conf`` file::

    [[local|localrc]]
    #Enable senlin
    enable_plugin senlin https://git.openstack.org/openstack/senlin

3. Run ``stack.sh``::

    $ ./stack.sh

Unit Test
---------

The unit tests can be executed directly from within this Senlin Dashboard plugin
project directory by using::

    tox

Switch to Angularized panels
----------------------------

The panels are ongoing to migrate to AngularJS based. If you would try them,
please copy ``_59_toggle_angular_senlin_dashboard.py.example`` to
``horizon/openstack_dashboard/local_settings.d/_59_toggle_angular_senlin_dashboard.py``
and restart Horizon.

Blueprints
----------

- Blueprints: https://blueprints.launchpad.net/senlin-dashboard

Bug Tracking
------------

- Bugs: https://bugs.launchpad.net/senlin-dashboard
