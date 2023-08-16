# Practical Workflow Example

Now let's consider a more complex scenario, one that covers the setup of
environments (using conda and pip) inside and outside containers.

Directory [`example_practical/`](example_practical/) is our workdirectory
for this example. The notebooks in there contain simple code cells, using
and tools specific to their corresponding environments, enough for checking
on the workflow.

Consider the following notebooks we want to include in our *book*:

1. (host) "this" environment
    - `this_env.ipynb`
1. (host) "new" environment
    - `new_env.ipynb`
1. jupyter container "X/Y:Z", *base* environment
    - `container_base_env`
1. jupyter container "X/Y:Z", "new" environment
    - `container_new_env`
1. jupyter container "X/Y:Z", *base* environment, plus package(s) ("abc", ...)
    - `packages_container_base_env`

## Command-steps

1. Run `this_env.ipynb`

    ```bash
    $ jcache notebook add this_env.ipynb

    Cache path: /planetary_data_stories/docs/example_practical/.jupyter_cache
    The cache does not yet exist, do you want to create it? [y/N]: y
    Adding: /planetary_data_stories/docs/example_practical/this_env.ipynb
    Success!

    $ jcache project execute

    Executing 1 notebook(s) in serial
    Executing: /planetary_data_stories/docs/example_practical/this_env.ipynb
    Execution Successful: /planetary_data_stories/docs/example_practical/this_env.ipynb
    Finished! Successfully executed notebooks have been cached.
    succeeded:
    - /planetary_data_stories/docs/example_practical/this_env.ipynb
    excepted: []
    errored: []
    ```

1. Run `new_env.ipynb`

    ```bash
    $ conda env create -f new_env.yml -n 'new_env'
    Preparing transaction: done
    Verifying transaction: done
    Executing transaction: done
    #
    # To activate this environment, use
    #
    #     $ conda activate new_env
    #
    # To deactivate an active environment, use
    #
    #     $ conda deactivate

    $ conda activate --stack 'new_env'

    $ pip install -y ipykernel
    Installing collected packages: ...
    Successfully installed ...

    $ python -m ipykernel install --user --name 'new_env'
    Installed kernelspec new_env in /Users/chbrandt/Library/Jupyter/kernels/new_env

    $ jcache notebook add new_env.ipynb
    Adding: /planetary_data_stories/docs/example_practical/new_env.ipynb
    Success!

    $ jcache notebook list
      ID  URI                                    Reader    Added             Status
    ----  -------------------------------------  --------  ----------------  --------
       1  docs/example_practical/this_env.ipynb  nbformat  2023-08-15 13:01  ✅ [1]
       2  docs/example_practical/new_env.ipynb   nbformat  2023-08-15 13:31  -

    $ jcache project execute
    Executing 1 notebook(s) in serial
    Executing: /planetary_data_stories/docs/example_practical/new_env.ipynb
    Execution Successful: /planetary_data_stories/docs/example_practical/new_env.ipynb
    Finished! Successfully executed notebooks have been cached.
    succeeded:
    - /planetary_data_stories/docs/example_practical/new_env.ipynb
    excepted: []
    errored: []

    $ conda deactivate
    ```

1. Run `container_base_env.ipynb`

    ```bash
    $ docker run -d --rm --name 'jupmin' -v "$PWD":"$PWD" 'jupyter/minimal-notebook'
    92c5f98c1b533

    $ docker exec -t -w "$PWD" 'jupmin' bash -ic "pip install jupyter-cache"
    Successfully installed click-8.1.6 jupyter-cache-0.6.1 nbclient-0.7.4 tabulate-0.9.0

    # FIRST CLEAN METADATA (kernelspec) from notebook
    $ docker exec -t -w "$PWD" 'jupmin' bash -ic "conda activate 'base' \
        && jcache notebook add 'container_base_env.ipynb' \
        && jcache project execute"

    $ docker stop 'jupmin'
    jupmin
    ```

1. Run `container_new_env.ipynb`

    ```bash
    $ # First, we have to remove metadata associated to kernel (jupyter-lab does this)
    $ jq 'del(.metadata.kernelspec)' container_new_env.ipynb > tmp.ipynb
    $ mv tmp.ipynb container_new_env.ipynb

    $ docker run -d --rm --name 'jupmin' -v "$PWD":"$PWD" 'jupyter/minimal-notebook'
    1a5dd6f089fc2

    $ docker exec -t 'jupmin' bash -ic \
        "conda env create -n 'tmp' -f $PWD/container_new_env.yml"

    $ docker exec -t 'jupmin' bash -ic \
        "conda activate 'tmp' && pip install jupyter-cache"
    Successfully installed jupyter-cache-0.6.1 ...

    <!-- $ docker exec -it jupmin bash -ic \
        "conda activate tmp \
        && pip install ipykernel \
        && python -m ipykernel install --user --name tmp" -->

    $ docker exec -t -w "$PWD" 'jupmin' bash -ic \
        "conda activate 'tmp' \
        && jcache notebook add 'container_new_env.ipynb' \
        && jcache project execute"

    $ docker stop 'jupmin'
    jupmin
    ```

1. Run `packages_container_base_env.ipynb`

    ```bash
    $ # First, we have to remove metadata associated to kernel (jupyter-lab does this)
    $ jq 'del(.metadata.kernelspec)' packages_container_base_env.ipynb > tmp.ipynb
    $ mv tmp.ipynb packages_container_base_env.ipynb

    $ docker run -d --rm --name 'jupmin' -v "$PWD":"$PWD" 'jupyter/minimal-notebook'
    6d8231be7c773

    $ docker exec -t 'jupmin' bash -ic \
        "conda activate 'base' && pip install jupyter-cache"
    (...)
    Successfully installed jupyter-cache-0.6.1 ...

    $ docker exec -t 'jupmin' bash -ic \
        "conda activate base \
        && python -m pip install -r $PWD/packages_container_base_env.txt"
    (...)
    Successfully installed sh-2.0.6

    $ docker exec -t -w "$PWD" 'jupmin' bash -ic \
        "conda activate 'base' \
        && jcache notebook add packages_container_base_env.ipynb \
        && jcache project execute"
    Adding: /planetary_data_stories/docs/example_practical/packages_container_base_env.ipynb
    Success!
    Executing 1 notebook(s) in serial
    Executing: /planetary_data_stories/docs/example_practical/packages_container_base_env.ipynb
    Execution Successful: /planetary_data_stories/docs/example_practical/packages_container_base_env.ipynb
    Finished! Successfully executed notebooks have been cached.
    succeeded:
    - /planetary_data_stories/docs/example_practical/packages_container_base_env.ipynb
    excepted: []
    errored: []

    $ docker stop 'jupmin'
    jupmin
    ```
