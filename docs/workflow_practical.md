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
    $ jcache project execute
    ```

1. Run `new_env.ipynb`
    ```bash
    $ conda create -n 'envY' -f envY.yml
    $ conda activate 'envY'
    $ conda install -y ipykernel
    $ python -m ipykernel install --user --name 'envY'

    $ jcache notebook add new_env.ipynb
    $ jcache project execute

    $ conda deactivate
    ```

1. Run `container_base_env.ipynb`
    ```bash
    $ docker run -d --rm --name 'contX' -v $PWD:/mnt/pwd --entrypoint /bin/bash 'X/Y:Z'

    $ docker exec 'contX' "cd /mnt/pwd \
    && conda activate 'base' \
    && jcache notebook add 'container_base_env.ipynb \
    && jcache project execute"

    $ docker stop 'contX'
    ```

1. Run `container_new_env.ipynb`
    ```bash
    $ docker run -d --rm --name 'contY' -v $PWD:/mnt/pwd --entrypoint /bin/bash 'X/Y:Z'

    $ docker exec 'contY' "conda create -n 'envY' -f /mnt/pwd/envY.yml"

    $ docker exec 'contY' "cd /mnt/pwd \
    && conda activate 'envY' \
    && jcache notebook add 'container_new_env.ipynb \
    && jcache project execute"

    $ docker stop 'contY'
    ```

1. Run `packages_container_base_env.ipynb`
    ```bash
    $ docker run -d --rm --name 'contZ' -v $PWD:/mnt/pwd --entrypoint /bin/bash 'X/Y:Z'

    $ docker exec 'contZ' "conda activate base && python -m pip install -r /mnt/pwd/req.txt"

    $ docker exec 'contZ' "cd /mnt/pwd \
    && conda activate 'base' \
    && jcache notebook add 'packages_container_base_env.ipynb \
    && jcache project execute"

    $ docker stop 'contZ'
    ```
