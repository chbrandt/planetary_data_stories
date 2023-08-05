# Workflow

[Jupyter-Book]: https://jupyter-book.org
[Jupyter-Cache]: https://jupyter-cache.readthedocs.io


Planetary Data Stories is created using [Jupyter-Book][].
The whole of the notebook is inside the [`book/`](../book) directory.

In general, simply running 
[`jupyter-book build book/`](https://jupyterbook.org/en/stable/start/build.html)
should build the book, but we need a specific workflow to build this book.

When we run `jupyter-book build`, in a default setup, it will run all notebooks
and markdown files into generating/building "the book".
*In our setup, though, we allow different notebooks to run in different (Python) 
environments.*
Because of that, we will break the building of the book in two major steps:

1. generate the results of (i.e., *run*) each notebook individually;
2. compile all results and markdown files (into the final book).

In technical terms, we will first use [Jupyter-Cache][] to run each notebook
in their own environments and *cache the results* for later use by Jupyter-Book.

## Example

If you're new here, you may want to read "[Example Workflow](example_workflow.md)"
as it provides the basic idea of the workflow we follow here.