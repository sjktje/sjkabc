**********************************
Contributing to the sjkabc project
**********************************

Getting a copy of the source code
=================================

The first step to contributing to sjkabc is to get a copy of the source code.
The easiest way of doing this is by using git. Browse the directory you want
the source code repository in and run the following command:

.. code-block:: console

    $ git clone https://github.com/sjktje/sjkabc.git

Setting up a virtualenv
=======================

Now that you've got a copy of the source code you can install sjkabc. The most
convenient way of doing this is by using a *virtual environment*. I prefer
using virtualenvwrapper_ for managing my virtual environments, and you probably
should too. 

I refer you to the virtualenvwrapper_ documentation for setting up a virtual
environment

.. note::
    Please note that sjkabc will only run under python 3, so when creating
    your virtualenvironment take care to make sure it'll use python 3. One
    way of doing this would be using the --python option:

    .. code-block:: console

        $ mkvirtualenv --python=python3 sjkabc

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/

Installing the development version
==================================

Assuming you called your virtual environment `sjkabc`, the following commands
will install the development version of sjkabc in your virtual environment.

.. code-block:: console

    $ cd path/to/sjkabc
    $ workon sjkabc
    $ git checkout develop
    $ python setup.py develop


Contributing changes
====================

The discussion and work on sjkabc is done through git_ and GitHub_. The project
utilise the git-flow_ branching scheme. Using git-flow is not difficult. Assuming
you have git-flow installed, the typical workflow for hacking on sjkabc is as
follows.

Start a new feature branch for whatever you are hacking on:

.. code-block:: console

    $ git flow feature start implement_parts

Hack away and commit changes just as usual. When done, publish your release
and ask for comments on the `issue tracker`_.


.. _GitHub: https://github.com/sjktje/sjkabc
.. _git: https://git-scm.com
.. _git-flow: https://github.com/nvie/gitflow
.. _`issue tracker`: https://github.com/sjktje/sjkabc/issues/

