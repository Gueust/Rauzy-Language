.. _getting_started:


***************
Getting started
***************

.. _installing-docdir:

Use of the package modeling
===========================

The whole project is using python3 and can be download from
https://github.com/Gueust/Rauzy-Language/.
The package :mod:`modeling` can be used both in the python3 shell or in a python
file.
In order to import the package, one can use::

  >>> from modeling import *
  
that imports modeling.model, modeling.library and modeling.core. In order not to
have to specify the modules prior to the classes and functions, one can use::

  >>> from modeling.model import *
  >>> from modeling.library import *
  >>> from modeling.core import *

To launch the module core and execute its main function, use::

  > python3 -m modeling.core

Creation of the documentation
-----------------------------

This documentation has been built using sphinx `sphinx <http://sphinx.pocoo.org/>`
. You may have shinx already installed -- you can check by doing::

  python -c 'import sphinx'

If that fails grab the latest version and install it with::

  > sudo easy_install -U Sphinx

Now you are ready to build the documentation using::

  > make html

in the doc/ directory.

