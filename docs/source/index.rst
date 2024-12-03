libgentools
============

    A Python library for downloading content from `Library Genesis <https://libgen.is/>`_.

The library serves as a backend for `libgenx <https://github.com/gaaldvd/libgenx>`_, a GUI/CLI application for using `LibGen <https://libgen.is/>`_, but it is available for implementation in any other Python project as well.

Developers are welcome to fork this repository on `GitHub <https://github.com/gaaldvd/libgentools>`_.

**Contents:**

.. :caption: Contents

- :ref:`Installation <installation>`
- :ref:`Usage <usage>`

  + :ref:`Classes <classes>`
  + :ref:`Exceptions <exceptions>`

- :ref:`Reporting errors <errors>`

.. toctree::
   :maxdepth: 2

   reference

.. _installation:

Installation
------------

It is always recommended to use a Python environment manager, like `pipenv <https://pipenv.pypa.io/en/latest/>`_:

.. code-block:: console

    $ pipenv install libgentools

But it is also possible to install the package system-wide:

.. code-block:: console

    $ pip install libgentools

Requirements
''''''''''''

- `Python 3+ <https://www.python.org/downloads/>`_
- `Beautiful Soup <https://pypi.org/project/beautifulsoup4/>`_

.. _usage:

Usage
-----

After installing from pip, import the library to your Python script:

.. code-block:: python

    import libgentools

or

.. code-block:: python

    from libgentools import SearchRequest, Results # ...

.. _classes:

Classes
'''''''

:ref:`SearchRequest <searchrequest>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class handles search requests and generates a list of results.

A new instance can be created with the ``query`` parameter. The query should be an author, title (or both) or an ISBN number:

.. code-block:: python

    request = SearchRequest('principles of geology')

The ``request.results`` variable now holds the search results as a list of Standard Entry Dictionaries (SEDs).

*Standard Entry Dictionary*:

.. code-block:: python

    entries = [{'id': 1234,
                'isbn': ["ISBN", "ISBN"],
                'auth': "Author",
                'title': "Title",
                'pub': "Publisher",
                'year': 1999,
                'pp': "Pages",
                'lang': "Language",
                'size': "Size",
                'ext': "Extension",
                'mirrors': ["url", "url"]}]

A new ``Results`` instance can be constructed from the ``request.results`` variable:

.. code-block:: python

    results = Results(request.results)

:ref:`Results <results>`
~~~~~~~~~~~~~~~~~~~~~~~~

The class stores and manages search results.

A new instance can be created from the ``results`` variable of a ``SearchRequest`` instance:

.. code-block:: python

    results = Results(request.results)

The results are now stored in the ``results.entries`` variable of the new instance as a list of SEDs.

:ref:`Filtering <filter-entries>`
"""""""""""""""""""""""""""""""""

The ``filter_entries`` method filters the results using a Standard Filter Dictionary and the filtering mode as parameters.

*Standard Filter Dictionary*:

.. code-block:: python

    filters = {'auth': "Author", 'ext': "Extension", 'year': "1999-2010"}

Every value must be a string! The following fields can be used in the filter:

- ``auth``: author
- ``title``: title
- ``year``: as an interval (e.g. "1999-2010") or exact year (e.g. "2000")
- ``lang``: use `standard language codes <https://www.iso.org/iso-639-language-code>`_
- ``ext``: use any of the popular formats (e.g. "pdf", "epub", "mobi", etc.)

The ``FILTERS`` dictionary can be used to interpret command line arguments in applications.

The second parameter is the filtering mode: ``"exact"`` or ``"partial"`` (the default is ``"partial"``). The method returns exact or partial matches based on this parameter.

The filtered results are returned by the method as a new ``Results`` instance:

.. code-block:: python

    filtered_results = results.filter_entries(filters, "exact")

:ref:`Downloading <download>`
"""""""""""""""""""""""""""""

Any entry from a list of results (SEDs) can be downloaded using the ``download`` method:

.. code-block:: python

    downloaded = results.download(entry, dirname(abspath(sys.argv[0])))

The first parameter is the entry (an SED), the second is the path where the file should be downloaded (in this case the location of the script - ``dirname()`` and ``abspath()`` can be imported from ``os.path``). The name of the downloaded file will be the LibGen ID of the entry. The value of the ``downloaded`` variable will be ``true`` if the download was successful or ``false`` otherwise.

.. _exceptions:

Exceptions
''''''''''

QueryError
~~~~~~~~~~

The constructor of the ``SearchRequest`` class raises this error if the ``query`` is empty or its length is less than three characters.

FilterError
~~~~~~~~~~~

The ``filter_entries`` method of the ``Results`` class raises this error if there is an invalid key in the filtering dictionary (validated by ``FILTERS``) or the year filter has a wrong format.

.. _errors:

Reporting errors
----------------

Any error can be reported through `e-mail <mailto:gaaldavid[at]tuta.io?subject=[GitHub]%20libgentools%20error>`_ with the exact error message and/or console screenshot. Alternatively, an `issue <https://github.com/gaaldvd/libgentools/issues>`_ can be opened.
