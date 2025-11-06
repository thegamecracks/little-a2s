Game-Specific Rules
===================

This provides a few classes for parsing some game-specific rules, in particular
Arma 3 and its relatives like DayZ, which uses the A2S_RULES response to send
a binarized list of game details, mods, and signatures.

.. versionadded:: 0.3.0

Arma 3
------

.. autoclass:: little_a2s.Arma3Rules
.. autoclass:: little_a2s.Arma3DLC
   :no-inherited-members:
.. autoclass:: little_a2s.Arma3Difficulty
.. autoclass:: little_a2s.Arma3Mod
