BalderHub CRUD
==============

**Test data management reliably - across any platform.**

``balderhub-crud`` is a BalderHub package that provides 
**ready-to-use, high-quality test scenarios and building blocks** for comprehensively validating 
**Create, Read, Update and Delete (CRUD)** operations on any kind of data.

Whether you are testing a REST API, a database, a mobile app backend, a desktop application, a file-based store, 
or an embedded device - this package lets you write powerful, reusable data-management tests **once** and run them
against completely different systems with minimal extra effort.

This is a BalderHub package for the `Balder <https://docs.balder.dev/>`_ test framework.
If you are new to Balder, please check out the `official documentation <https://docs.balder.dev>`_ first.


What you will find in this package
----------------------------------

- **Ready-to-use Scenarios** - Pre-built Balder scenarios for all essential CRUD operations:

  - Single-item: **Create**, **Read**, **Update** (Delete coming soon)  
  - Multi-item: **Read** operations  
  - Advanced **Triangle scenarios** (modify on one device, verify on another - perfect for client-server or distributed systems)

- **Feature Building Blocks** - Clean base feature classes you only need to implement for your specific System Under Test (SUT):

  - ``SingleCreatorFeature``, ``SingleReaderFeature``, ``SingleUpdaterFeature``  
  - ``MultipleReaderFeature``  
  - Support for both direct devices and separate “Point of Truth” verification devices

- **Strong Data Modeling** (powered by ``balderhub-data``) - Pydantic-style ``DataItem`` models with automatic handling of:

  - Mandatory / optional fields  
  - Default values  
  - Special markers: ``UNSET`` and ``NOT_DEFINABLE``  
  - Smart automatic example generation (valid, invalid, and edge-case data)

- **Validation & Utilities** - Comprehensive helpers for before/after state checks, field-level comparison, diffing,
  success/error handling, and cross-device consistency verification.

.. note::
   This package is still under active development. Contributions are very welcome!  
   See the `GitHub repository <https://github.com/balder-dev/balderhub-crud/>`_.


.. toctree::
   :maxdepth: 2

   installation.rst
   topic_intro.rst
   scenarios.rst
   features.rst
   examples.rst
   utilities.rst
