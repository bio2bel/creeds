Bio2BEL CREEDS |build|
==================================================
CRowd Extracted Expression of Differential Signatures

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
``bio2bel_creeds`` can be installed easily from
`PyPI <https://pypi.python.org/pypi/bio2bel_creeds>`_
with the following code in your favorite terminal:

.. code-block:: sh

    $ python3 -m pip install bio2bel_creeds

or from the latest code on `GitHub <https://github.com/bio2bel/creeds>`_ with:

.. code-block:: sh

    $ python3 -m pip install git+https://github.com/bio2bel/creeds.git

Setup
-----
CREEDS can be downloaded and populated from either the
Python REPL or the automatically installed command line utility.

Python REPL
~~~~~~~~~~~
.. code-block:: python

    >>> import bio2bel_creeds
    >>> creeds_manager = bio2bel_creeds.Manager()
    >>> creeds_manager.populate()

Command Line Utility
~~~~~~~~~~~~~~~~~~~~
.. code-block:: sh

    bio2bel_creeds populate


.. |build| image:: https://travis-ci.com/bio2bel/creeds.svg?branch=master
    :target: https://travis-ci.com/bio2bel/creeds
    :alt: Build Status

.. |documentation| image:: http://readthedocs.org/projects/bio2bel-creeds/badge/?version=latest
    :target: http://bio2bel.readthedocs.io/projects/creeds/en/latest/?badge=latest
    :alt: Documentation Status

.. |pypi_version| image:: https://img.shields.io/pypi/v/bio2bel_creeds.svg
    :alt: Current version on PyPI

.. |coverage| image:: https://codecov.io/gh/bio2bel/creeds/coverage.svg?branch=master
    :target: https://codecov.io/gh/bio2bel/creeds?branch=master
    :alt: Coverage Status

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/bio2bel_creeds.svg
    :alt: Stable Supported Python Versions

.. |pypi_license| image:: https://img.shields.io/pypi/l/bio2bel_creeds.svg
    :alt: MIT License
