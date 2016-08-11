================
Senlin Dashboard
================

Senlin Management Dashboard

Devstack Installation
---------------------


1. Download DevStack::

    $ git clone https://git.openstack.org/openstack-dev/devstack
    $ cd devstack

2. Add following repo as external repositories into your ``local.conf`` file::

    [[local|localrc]]
    #Enable senlin
    enable_plugin senlin https://git.openstack.org/openstack/senlin
    #Enable senlin-dashboard
    enable_plugin senlin-dashboard https://git.openstack.org/openstack/senlin-dashboard 

3. Run ``stack.sh``::

    $ ./stack.sh

Unit Test
---------

The unit tests can be executed directly from within this Senlin Dashboard plugin
project directory by using::

    tox

Blueprints
----------

- Blueprints: https://blueprints.launchpad.net/senlin-dashboard

Bug Tracking
------------

- Bugs: https://bugs.launchpad.net/senlin-dashboard
