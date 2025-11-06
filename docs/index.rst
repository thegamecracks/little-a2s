little-a2s documentation
========================

|pypi| |readthedocs| |publish| |pytest| |pyright-lint| |ruff-check| |ruff-format|

.. |pypi| image:: https://img.shields.io/pypi/v/little-a2s?style=flat-square&logo=pypi
   :target: https://pypi.org/project/little-a2s/

.. |readthedocs| image:: https://readthedocs.org/projects/little-a2s/badge/?style=flat-square
   :target: http://little-a2s.readthedocs.io/

.. |publish| image:: https://img.shields.io/github/actions/workflow/status/thegamecracks/little-a2s/publish.yml?style=flat-square&logo=uv&label=build
   :target: https://docs.astral.sh/uv/

.. |pytest| image:: https://img.shields.io/github/actions/workflow/status/thegamecracks/little-a2s/pytest.yml?style=flat-square&logo=pytest&label=tests
   :target: https://docs.pytest.org/

.. |pyright-lint| image:: https://img.shields.io/github/actions/workflow/status/thegamecracks/little-a2s/pyright-lint.yml?style=flat-square&label=pyright
   :target: https://microsoft.github.io/pyright/#/

.. |ruff-check| image:: https://img.shields.io/github/actions/workflow/status/thegamecracks/little-a2s/ruff-check.yml?style=flat-square&logo=ruff&label=lints
   :target: https://docs.astral.sh/ruff/

.. |ruff-format| image:: https://img.shields.io/github/actions/workflow/status/thegamecracks/little-a2s/ruff-format.yml?style=flat-square&logo=ruff&label=style
   :target: https://docs.astral.sh/ruff/

A synchronous and sans-I/O library implementing the A2S Valve Source Query protocol.

.. code-block:: python

   from little_a2s import A2S

   with A2S.from_addr("example.com", 27015, timeout=1) as a2s:
       print(a2s.info())
       print(a2s.players())
       print(a2s.rules())

.. toctree::
   :maxdepth: 2

Installation
------------

This project requires Python 3.11 or newer. Install it from PyPI by using pip:

.. code-block:: sh

   $ python3 -m venv
   $ .venv/bin/activate
   (.venv) $ pip install little-a2s

Synchronous Clients
-------------------

.. autoclass:: little_a2s.A2S
.. autoclass:: little_a2s.A2SGoldsource
