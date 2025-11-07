Asynchronous Clients
====================

This covers the asynchronous I/O client provided by little-a2s.

little-a2s only provides an asyncio client. If you need to integrate with a
different event loop such as `Trio`_, `anyio`_, or `gevent`_, you can use
the :doc:`Sans-I/O interface </protocol>` to build your own client.

.. _Trio: https://trio.readthedocs.io/
.. _anyio: https://anyio.readthedocs.io/
.. _gevent: https://www.gevent.org/

.. versionadded:: 0.5.0

.. autoclass:: little_a2s.AsyncA2S
   :no-inherited-members:
.. autoclass:: little_a2s.AsyncA2SGoldsource
   :no-inherited-members:
