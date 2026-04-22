Scenarios
*********

Scenarios describe **what you need**. They define the tests and the necessary devices for them. Here you can find all
scenarios that are implemented in this BalderHub package.

Every CREATE/UPDATE/DELETE scenario exists in two variants: a NORMAL version and a TRIANGLE version.

In the **NORMAL** version, a single device handles both the creation, updating and deletion of the data as well as
reading the data back.

The **TRIANGLE** version differs in that it involves three devices. One device is responsible for creating, updating
or deleting the data, while a second device reads the data bag. Both devices are connected to the device or system
under test.


SINGLE Read Scenario
====================

.. image:: _static/ScenarioSingleRead.svg
    :align: center
    :alt: Graphical represenation of the `ScenarioSingleRead`

.. autoclass:: balderhub.crud.scenarios.ScenarioSingleRead
    :members:

SINGLE Create Scenario
======================

Normal SINGLE Create Scenario
-----------------------------

.. image:: _static/ScenarioSingleCreate.svg
    :align: center
    :alt: Graphical represenation of the `ScenarioSingleCreate`

.. autoclass:: balderhub.crud.scenarios.ScenarioSingleCreate
    :members:

Triangle SINGLE Create Scenario
-------------------------------

.. image:: _static/ScenarioTriangleSingleCreate.svg
    :align: center
    :alt: Graphical represenation of the `ScenarioTriangleSingleCreate`

.. autoclass:: balderhub.crud.scenarios.ScenarioTriangleSingleCreate
    :members:

SINGLE Update Scenario
======================

Normal SINGLE Update Scenario
-----------------------------

.. image:: _static/ScenarioSingleUpdate.svg
    :align: center
    :alt: Graphical represenation of the `ScenarioSingleUpdate`

.. autoclass:: balderhub.crud.scenarios.ScenarioSingleUpdate
    :members:

Triangle SINGLE Update Scenario
-------------------------------

.. image:: _static/ScenarioTriangleSingleUpdate.svg
    :align: center
    :alt: Graphical represenation of the `ScenarioTriangleSingleUpdate`

.. autoclass:: balderhub.crud.scenarios.ScenarioTriangleSingleUpdate
    :members:

SINGLE Delete Scenario
======================

.. note::
    The DELETION scenarios are not fully developed.

MULTIPLE Read Scenario
======================

.. image:: _static/ScenarioMultipleRead.svg
    :align: center
    :alt: Graphical represenation of the `ScenarioMultipleRead`

.. autoclass:: balderhub.crud.scenarios.ScenarioMultipleRead
    :members:

MULTIPLE Create Scenario
========================

.. note::
    The MULTIPLE CREATE scenarios are not fully developed.

MULTIPLE Update Scenario
========================

.. note::
    The MULTIPLE UPDATE scenarios are not fully developed.

MULTIPLE Delete Scenario
========================

.. note::
    The DELETION scenarios are not fully developed.
