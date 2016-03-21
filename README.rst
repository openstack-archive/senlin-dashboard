================
Senlin Dashboard
================

Senlin Management Dashboard

Devstack Installation
---------------------

By default, the devstack will install senlin dashboard while you enable
senlin in devstack.

1. Download DevStack::

     git clone https://git.openstack.org/openstack-dev/devstack
     cd devstack

2. Add this repo as an external repository into your ``local.conf`` file::

     [[local|localrc]]
     enable_plugin senlin https://git.openstack.org/openstack/senlin

3. Run ``stack.sh``.

Unit Test
---------

The unit tests can be executed directly from within this Senlin Dashboard plugin
project directory by using::

    ./run_tests.sh

Blueprints
----------

- Blueprints: https://blueprints.launchpad.net/senlin-dashboard

Bug Tracking
------------

- Bugs: https://bugs.launchpad.net/senlin-dashboard
