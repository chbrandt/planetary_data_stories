"""
Handles running notebooks in their required environments

Especifically, this tool is doing:
- parse notebook-dirs config files ('env.cfg')
- command setup of environment
    * docker container
    * conda environment
    * pip requirements
- run notebook(s) through jupyter-cache

> Does NOT handle jupyter-book (command).
"""
# from configparser import ConfigParser
# parser = ConfigParser(empty_lines_in_values=False)

# from benedict import benedict

from invoke import task

_NB_LIST = []

@task
def add(ctx, path):
    """
    Add notebook or directory (path) to the list of notebooks to run

    Args:
    - path : path-like string
    """
    nblist = []
    # Resolve path, parse corresponding config file, include in the list
    _NB_LIST.extend(nblist)
    msg = f"Notebooks {nblist} added to the project"
    print(msg)

@task
def run(ctx, path='all'):
    """
    Run notebook(s) in path

    Input:
    - path : path-like string
    """
    # Run each notebook in the list in their corresponding environment
    # - prepare environment

def _parse_config(config_path):
    """
    Input:
    - config_path : path-like string
        Path to a config file ('env.cfg')
    Output:
    - return a ConfigParser object
    """
    raise NotImplementedError

def _setup_environment(container=None, environment=None, requirements=None):
    """
    Setup environment (container, packages)

    Input:
    - container : string
        Name of the container image to instantiate
    - environment : string
        Name of the conda environment, or environment filename to use
    - requirements : string or list of strings
        Requirements filename, package name, or string of packages names

    Output:
        If image 'container' input given, return name of running container.
        Raises 'RuntimeError' if setup failed, return True otherwise.
    """
    raise NotImplementedError
