r"""
.. module:: modeling

The modeling package provides an API to create and modify models that use
the Rauzy Language. Most of the API functions are type-checked at runtime to
ensure the types of the inputs. If one gets an exception related with types, one
should look at the documentation for the types asked by a the function.

To launch the modules contained in the modeling package as simple scripts use:

>>> python3 -m modeling.core

for the core module for example.
"""

__all__ = ["core", "model", "library"]
