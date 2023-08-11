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

If you're new to jupyter-book and jupyter-cache, you may want to read 
"[Example Workflow](example_workflow.md)" first
as it provides the basic idea of the workflow we follow here.


## Source-files structure

As commented above and initially explained in the "Example Workflow",
different notebooks (may/will) demand different library, consequently,
different environments.
And splitting the workflow into a "compilation" phase -- *jupyter-cache* --
and an "assembly" phase -- *jupyter-book build* -- solves the limitations
otherwise imposed.

To automated the whole process so we can say "build planetary-data-stories",
we need to define a structure of files and directories indicating which
environment goes with which environment.

### Docker containers

When we talk about *environments* running a notebook, we must include
environments that are *inside a container*.
For instance, many of the notebooks making into this book are meant to
run in an ISIS environment defined inside our group's 
[Docker-ISIS](https://github.com/europlanet-gmap/docker-isis)

### Conda environments

The environments here are always defined as Conda environments, for the
time being we do not support other environment managers.

### Environments, packages, containers possibilities

The following situations for running a notebook should be supported:
- notebook runs in an environment inside a container;
- notebook runs in an environment in the host system;
- notebook runs in a pre-defined environment, with a few new packages.

> [!NOTE]
> Since these notebooks are used in a context of "reproducible results"
> the amount of (new) environments is expected to be minimal.
 
In the repository, notebooks inside the same directory will share
the same environment