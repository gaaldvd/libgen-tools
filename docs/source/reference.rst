Reference
=========

    A technical reference for the `libgentools <https://github.com/gaaldvd/libgentools>`_ package.

**Contents:**

- :ref:`make_soup() function <make-soup>`
- :ref:`SearchRequest class <searchrequest>`

  + :ref:`get_results() method <get-results>`
  + :ref:`create_entry_list() method <create-entry-list>`

- :ref:`Results class <results>`

  + :ref:`filter_entries() method <filter-entries>`
  + :ref:`get_download_urls() method <get-download-urls>`
  + :ref:`download() method <download>`

- :ref:`QueryError exception <queryerror>`
- :ref:`FilterError exception <filtererror>`

----------

.. _make-soup:

.. autofunction:: libgentools.make_soup

.. _searchrequest:

SearchRequest class
-------------------

.. autoclass:: libgentools.SearchRequest

.. automethod:: libgentools.SearchRequest.__init__

.. _get-results:

.. automethod:: libgentools.SearchRequest.get_results

.. _create-entry-list:

.. automethod:: libgentools.SearchRequest.create_entry_list

.. _results:

Results class
-------------

.. autoclass:: libgentools.Results

.. automethod:: libgentools.Results.__init__

.. _filter-entries:

.. automethod:: libgentools.Results.filter_entries

.. _get-download-urls:

.. automethod:: libgentools.Results.get_download_urls

.. _download:

.. automethod:: libgentools.Results.download

.. _queryerror:

QueryError exception
--------------------

.. autoexception:: libgentools.QueryError

.. _filtererror:

FilterError exception
---------------------

.. autoexception:: libgentools.FilterError
