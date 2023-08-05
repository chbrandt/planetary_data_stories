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

To simplify the understanding of the basic workflow we go through, let's use
a generic example.

Consider in our `book/` directory we had the following files:

- `intro.md`: a markdown file with some welcoming message;
- `notebooks/requests.ipynb`: a notebook dependent on environment `requests`;
- `notebooks/scipy.ipynb`: a notebook dependent on environment `scipy`;
- `_config.yml`: jupyter-book config file;
- `_toc.yml`: jupyter-book toc file.

The content of `requests.ipynb` is a cell with a simple import:
```python
import requests
print(requests.__version__)
```

Notebook `scipy.ipynb`, has cell with its particualr import:
```python
import scipy
print(scipy.__version__)
```

Jupyter-book `_config.yml` file is largely default but the following options:
```yaml
# See https://jupyterbook.org/content/execute.html
execute:
  execute_notebooks: cache
  cache: .jupyter_cache/
```
Which will constrain `jupyter-book` to NOT run notebooks on its own 
but use *only* those in the *cache* (generated previously by `jupyter-cache`).

Jupyter-book `_toc.yml` is the default, by defaul it will include everything
in "the book" directory.

    Jupyter-book default files are gererated when we create a template notebook 
    (see [Anatomy of a book](https://jupyterbook.org/en/stable/start/create.html#anatomy-of-a-book)):
    ```bash
    jupyter-book create "my_book"
    ```

### Notebook environments

The environments `requests` and `scipy`, where the notebooks run, need to have
`jupyter-cache` installed (besides the required packages):
```bash
conda create -n requests -y requests jupyter-cache
conda create -n scipy -y scipy jupyter-cache
```

### Jupyter-Cache

For each notebook, we add end execute that through `jupyter-cache`, from
there respective environments.
We run them all using the same cache, as stated in `_config.yml`,
`.jupyter_cache/`.
Inside the book directory (eg, "my_book/"),
```bash

