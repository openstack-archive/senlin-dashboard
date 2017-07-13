============
Installation
============

Before install the Senlin Dashboard, setup the Horizon.
To setup the Horizon, see
`Installation Guide
<https://docs.openstack.org/horizon/latest/install/index.html>`__
in the Horizon documentation.

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
