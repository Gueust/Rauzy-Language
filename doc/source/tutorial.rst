********
Tutorial
********

An example
==========

We are going to model the following diagram:

.. image:: _static/diagrams-example-model.png

The equivalent representation of this model is available in :file:`tutorial-example.py`
at the root of the project directory.

This example also shows the behavior of the abstractions functions.

.. literalinclude:: ../../tutorial-example.py

An second example
==========

We demonstrate the functiosn that create, abstract, flatten and compare objects in :file:`tutorial-example-abst_flat_comp.py`
at the root of the project directory.

.. literalinclude:: ../../tutorial-example-abst_flat_comp.py

All functionalities
===================

All API functions are described in :mod:`modeling`. However, the most high level
functionalities are worth being highlighted:

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
  An example applied to the diagram upper in this page is included in
  tutorial-example.py
- The :meth:`keyword_abstraction(key, value) <modeling.core.Object.keyword_abstraction>`
  abstraction function allows a more general abstraction. It abstracts an object
  keeping only sub-objects containing the `key` => `value` property. In a more
  general case, we should give a key and a boolean function and the abstraction 
  would keep all the objets which have this `key` => `value` in their properties
  and for which f(value) returns true.
- The :meth:`flatten() <modeling.core.Object.flatten>` returns an object, which stores
  in its properties group the entire sub-hierarchy of objects and their respective
  properties. An example that applies this function can be found in
  tutorial-example-abst_flat_comp.py
- The :meth:`flatten_with_extends(library) <modeling.core.Object.flatten_with_extends>` returns
  a similar object as the previous method, but also includes the objects and properties
  that exist within any objects that are extended within any item in the object hierarchy.
  An example that applies this function can be found in tutorial-example-abst_flat_comp.py
- The :meth:`compare(obj) <modeling.core.Object.compare>` displays to the user the items,
  both objects and properties, that are found exclusively in one of the two objects that
  are being compared as well as the properties that are shared but that correspond to a
  different value. An example that applies this function can be found in
  tutorial-example-abst_flat_comp.py
- The :meth:`compare_with_extends(obj, library) <modeling.core.Object.compare_with_extends>`
  displays to the user the items, both objects and properties, that are found exclusively
  in one of the two objects that are being compared as well as the properties that are
  shared but that correspond to a different value. An example that applies this function
  can be found in tutorial-example-abst_flat_comp.py
  
  
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
