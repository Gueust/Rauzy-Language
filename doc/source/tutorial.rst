********
Tutorial
********

An example
==========

We are going to model the following diagram:

.. image:: _static/diagrams-example-model.png

The structured will be kept but names may change little.

All functionalities
===================

Further development
===================

A large number of potential errors are managed using exceptions. However, some
of them are not taken into account, or silently corrected.

For instance, in case of multiple definition of the same key in a json object,
the default dehavior of the :mod:`json` parser is to keep the last value.

The management of all these errors not being the point of the project, they have
not been exhaustively listed and taken into account.
