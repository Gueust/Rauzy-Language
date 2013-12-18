********
Tutorial
********

An example
==========

We are going to model the following diagram:

.. image:: _static/diagrams-example-model.png

The equivalent representation of this model is available in tutorial-example.py
at the root of the project directory.

All functionalities
===================

All API functions are described in :mod:`modeling`. However, the most high level
functionalities to are worth being highlighted:

- The :meth:`~modeling.model.Model.load` and :meth:`~modeling.model.Model.save`
  functions allows to load model from files and to write them to files.
- The :meth:`merge(lib1, lib2) <modeling.library.Library.merge>` function allows
  to merge two libraries into one.
- The :meth:`lookup_obj(name) <modeling.core.Object.lookup_obj>` returns an
  object having the name `name` in the sub-hierarchy. In particular, if there is
  only one object for a given name, it allows to look up for this particular
  object.
- The :meth:`lookup_obj_parent(name) <modeling.core.Object.lookup_obj_parent>`
  funtion returns the parent of the object named `name` and None is it does not
  exist. In can be particulaly usefull to rename a given object for instance.
- The :meth:`abst_obj(level) <modeling.core.Object.abst_obj>` creates an
  abstraction of a given object keeping only the objects that are at most at
  the `level` sub-hierarchy. In particular, after having removed the objects
  deeper than `level` it calls :meth:`~modeling.core.Object.remove_unvalid_relations`
  that removes relations made unvalid because of the deletion of some objects.


Further development
===================

A large number of potential errors are managed using exceptions. However, some
of them are not taken into account, or silently corrected.
For instance, in case of multiple definition of the same key in a json object,
the default behavior of the :mod:`json` parser is to keep the last value. This
default behavior is inherited by our parser that does not raise en error if a key
is defined more than once in the json representation of a Rauzy model.

The management of all these errors not being the point of the project, they have
not been exhaustively listed and taken into account. However we can note that:

- The full correctness of any Rauzy objects designed using the API is not
  ensured. It is possible to do so maintaining invariants but it adds huge
  constraints on the use of the API functions. For instance, in order to ensure
  that any given relation links existing objects, a relation should be added
  first and then its toSet and fromSet fields filled.

  For that reason, correct models are the responsability of the user. However,
  there is some support to inform the user that his or her actions may lead to
  inconsistent models (for example, setting the toSet or fromSet of a relation
  without having added the relation in an object will raise a warning).
