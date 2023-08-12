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

In the [Example](#example) workflow, all notebooks are in the same directory
and we *"jupyter-cache run"* each of them manually.
For our book, though, we need some organization because we want to automate
the building process because:

1. simplicity
1. scalability

> [!NOTE]
> The structure of the content in the book is dictated by `_toc.yml`,
> *not* the structure of files in the repository. Meaning, we are
> free to organize files however fits better the workflow.

As a general rule, notebooks depending on the same environment
should be placed under the same directory. Inside the directory,
a config file specifies details about the environment to run the
notebooks.

### Docker containers

When we talk about *environments* running a notebook, we must include
environments that are *inside a container*.
For instance, many of the notebooks making into this book are meant to
run in an ISIS environment defined inside our group's
[Docker-ISIS](https://github.com/europlanet-gmap/docker-isis)

### Conda environments

The environments here are always defined as Conda environments, for the
time being we do not support other environment managers.

### Environments, packages, containers

The following situations for running a notebook should be supported:

- notebook runs in an environment inside a container;
- notebook runs in an environment in the host system;
- notebook runs in a pre-defined environment, with a few new packages.

> [!NOTE]
> Since these notebooks are used in a context of "reproducible results"
> the amount of (new) environments is expected to be minimal.
> And many of them inside containers.

Suppose we have the following notebooks composing our book:

- "download_pds_images.ipynb": depends only on Python Requests library
    > Next to this notebook, we need a `requirements` or `environment`
    > file stating the dependency on `requests` (eg, version `2.31`):
    > ```
    > requests==2.31
    > ```

- "transform_images.ipynb": depends on USGS/ISIS tools and `npt` library
    > This notebook runs on our `docker-isis` container, in an environment
    > with the `npt` library installed. In this case, we have to specify
    > the container, and the python lib to install:
    > ```
    > container = gmap/jupyter-isis:7.1.0
    > environment = npt
    > [npt]
    > file = environment.yml
    > ```

- "mosaic_images.ipynb": depends on Python GIS (GDAL, Rasterio)
    > This notebook runs on our "gispy" container (`base` environ):
    > ```
    > container = gmap/jupyter-gispy
    > ```
