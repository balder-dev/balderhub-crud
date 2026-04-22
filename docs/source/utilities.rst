Utilities
*********

This section shows general objects and helper functions that are used with this package.

General
=======

.. autoclass:: balderhub.crud.lib.utils.unset._UNSET_TYPE
        :members:


Field Callbacks
===============

Field Callbacks are used to read/write data field values to a remote device.

.. autoclass:: balderhub.crud.lib.utils.field_callbacks.base_field_callback.BaseFieldCallback
    :members:

.. autoclass:: balderhub.crud.lib.utils.field_callbacks.FieldCollectorCallback
    :members:

.. autoclass:: balderhub.crud.lib.utils.field_callbacks.FieldFillerCallback
    :members:

.. autoclass:: balderhub.crud.lib.utils.field_callbacks.Nested
    :members:

Exceptions
==========

.. autoclass:: balderhub.crud.lib.utils.exceptions.CallbackExecutionError
    :members:
