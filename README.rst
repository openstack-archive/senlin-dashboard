================
Senlin Dashboard
================

Senlin Management Dashboard

* Free software: Apache license
* Source: http://git.openstack.org/cgit/openstack/senlin-dashboard
* Bugs: http://bugs.launchpad.net/senlin-dashboard

Installation instructions
-------------------------

Begin by cloning the Horizon and Senlin Dashboard repositories::

    git clone https://git.openstack.org/openstack/horizon
    git clone https://git.openstack.org/openstack/senlin-dashboard

Create a virtual environment and install Horizon dependencies::

    cd horizon
    python tools/install_venv.py

Set up your ``local_settings.py`` file::

    cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

Open up the copied ``local_settings.py`` file in your preferred text
editor. You will want to customize several settings:

-  ``OPENSTACK_HOST`` should be configured with the hostname of your
   OpenStack server. Verify that the ``OPENSTACK_KEYSTONE_URL`` and
   ``OPENSTACK_KEYSTONE_DEFAULT_ROLE`` settings are correct for your
   environment. (They should be correct unless you modified your
   OpenStack server to change them.)


Install Senlin Dashboard with all dependencies in your virtual environment::

    tools/with_venv.sh pip install -e ../senlin-dashboard/

And enable it in Horizon::

    cp ../senlin-dashboard/_50_senlin.py.example openstack_dashboard/local/enabled/_50_senlin.py


Starting the app
----------------

If everything has gone according to plan, you should be able to run::

    ./run_tests.sh --runserver 0.0.0.0:8080

and have the application start on port 8080. The horizon dashboard will
be located at http://localhost:8080/

Unit testing
------------

The unit tests can be executed directly from within this Senlin Dashboard plugin
project directory by using::

    cd ../senlin-dashboard
    ./run_tests.sh

This is made possible by the dependency in test-requirements.txt upon the
horizon source, which pulls down all of the horizon and openstack_dashboard
modules that the plugin uses.
