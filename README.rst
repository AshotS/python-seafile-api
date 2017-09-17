python-seafile-api
======

This is fork of https://github.com/haiwen/python-seafile with support some additional features.

Requirements
------
- Python 3.x
- `Requests <http://www.python-requests.org/en/latest/>`

Getting started
---------------

The documentation gives some examples in more detail, as well as a full API specification, but here are the basics to get you started:

.. code:: python

    import seafileapi

    client=seafileapi.connect('http://address:8000', 'admin@email.com', 'password')

    client.admin.list_accounts()

    Out[17]:
    [SeafileAccount<id=1, user=sdsd@sdfsds.ru>,
     SeafileAccount<id=62, user=test@test.com>,
     SeafileAccount<id=104, user=ddd1@ddd.ru>]

    client.repos.create_repo('new_repo')

    Out[19]: SefileRepo<id=63ca0c53-7d8c-470c-b0a9-260afa755079, name=new_repo>


API Documentation
------
https://manual.seafile.com/develop/web_api_v2.1.html
