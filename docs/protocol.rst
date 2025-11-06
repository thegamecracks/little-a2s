Protocol Classes
================

This covers the Sans-I/O interface provided by little-a2s.

Protocols
---------

.. autoclass:: little_a2s.A2SClientProtocol
.. autoclass:: little_a2s.A2SGoldsourceClientProtocol

Events
------

.. autoclass:: little_a2s.Event
.. autoclass:: little_a2s.ClientEvent
.. autoclass:: little_a2s.ClientEventChallenge
.. autoclass:: little_a2s.ClientEventGoldsourceInfo
.. autoclass:: little_a2s.ClientEventInfo
.. autoclass:: little_a2s.ClientEventPlayers
.. autoclass:: little_a2s.ClientEventRules
.. autoclass:: little_a2s.Environment
   :no-inherited-members:
.. autoclass:: little_a2s.ExtraInfo
.. autoclass:: little_a2s.GoldsourceMod
.. autoclass:: little_a2s.GoldsourceModDLL
   :no-inherited-members:
.. autoclass:: little_a2s.GoldsourceModType
   :no-inherited-members:
.. autoclass:: little_a2s.Player
.. autoclass:: little_a2s.ServerType
   :no-inherited-members:
.. autoclass:: little_a2s.VAC
   :no-inherited-members:
.. autoclass:: little_a2s.Visibility
   :no-inherited-members:

Headers
-------

.. autoclass:: little_a2s.Header
.. autoclass:: little_a2s.HeaderType
   :no-inherited-members:
.. autoclass:: little_a2s.SimpleHeader
.. autoclass:: little_a2s.MultiHeader
.. autoclass:: little_a2s.Compression
.. autoclass:: little_a2s.MultiGoldsourceHeader

Packets
-------

.. autoclass:: little_a2s.Packet
.. autoclass:: little_a2s.ClientPacket
.. autoclass:: little_a2s.ClientPacketInfo
.. autoclass:: little_a2s.ClientPacketPlayers
.. autoclass:: little_a2s.ClientPacketRules

Utilities
---------

.. autoclass:: little_a2s.MultiPartResponse
.. autoclass:: little_a2s.Readable
.. autoclass:: little_a2s.Reader
.. autofunction:: little_a2s.filter_type
.. autofunction:: little_a2s.first
.. autofunction:: little_a2s.last
