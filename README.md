# DeFyes

DeFyes is a Python library designed to track DeFi portfolios across multiple protocols.
This library serves as a versatile toolkit to retrieve DeFi positions' underlying
assets and financial metrics.

The project is currently undergoing active development, so we expect some backward incompatibility changes until we stabilize the API. We encourage you to stay engaged with the project’s updates and contribute to its evolution.

Some protocols supported: Aave v2 and v3, Lido, Compound v2 and v3, Balancer, Curve, Maker and more.
While cross-chain functionalities are supported, currently most integrations are focused on Ethereum
and Gnosis Chain.

## Install

When using `defyes` as a library, you have two way to install it:
```sh
pip install . 'defyes[all]'
```
or, if you experiment dependencies conflicts, you can take control over some dependencies version by removing `[all]`
but specifying each missing dependencie.
```sh
pip install . 'defyes'
pip install "karpatkit @ git+https://github.com/karpatkey/karpatkit.git@another_specific_version"
```
where `another_specific_version` should be a git reference (tag, hash, branch).

Have a look `all` in the [pyproject.toml](pyproject.toml) file, `[project.optional-dependencies]` section.

> Take into account that installing just `defyes` without `defyes[all]` is an incompleted instalation.


## Configuration 

- First you will have to copy, rename and modify the [config.json](https://github.com/karpatkey/defyes/blob/main/example_config.json)

- You should provide `RPC` endpoints and `EXPLORER API KEYS`

- You should set the env `CONFIG_PATH` env with the config.json's absolute path.

## Cache

To reduce the number of calls to RPC endpoints, and thus significantly speed up the functions, defyes implements a cache where the result of some web3 calls are stored.
If the same web3 function is called, with the very same arguments, its result will be retrieved from the cache.

By default the cache is enabled and caches all calls to web3 'eth_call' when a block other than 'latest' is specified.
In practice this means that the following example calls will be cached:

    ```python
    chef_contract.functions.totalAllocPoint().call(block_identifier=1560000)

    chef_contract.functions.poolLength().call(block_identifier=block)

    token_contract.functions.decimals().call(block_identifier=block)
    ```

The following calls will not be cached:

    ```python
    chef_contract.functions.poolLength().call(block_identifier='latest')

    token_contract.functions.decimals().call()

    web3.eth.get_balance()

    contract.functions.updateValue(43).transact()

    ```

This functionality of the cache is very useful as long as the same block can be used, even if only for a while, since successive calls will bring the responses from the cache. This is very useful for example in tests or when developing.

There are some calls that are expected to always return the same value from the blockchain.
For example, `token.contract.decimals.call(block_identifier=block)`, will return the same value if the block is equal or greater than the block the contract was deployed.
For this type of calls, which return something constant in time, the automatic cache is  not useful because if a block is specified, the value will only be used for that block. And if 'latest' is specified, it is automatically excluded from the cache.
For these cases the const_call() helper function is used.

### `const_call()` helper

The `const_call()` function forces the caching of a `.call()` without defining a block. Thus subsequent calls to `const_call()` will return the same result even if the block is different from the block in which the result was cached.
Warning: if a call is made after caching using a block prior to the contract creation, `const_call()` will reuse the locally stored value instead of returning an error.

Example usage:

    ```
    const_call(token_contract.functions.decimals())

    const_call(pool_contract.functions.token0())
    ```

### Cache config

By default the cache is stored in a non persistent directory `/tmp/kkit/`.
To change the directory use the environment variable `KKIT_CACHE_DIR=/path/to/dir`.

To disable the cache define the `KKIT_CACHE_DISABLE` environment variable.

To wipe the cache use the env var `KKIT_CACHE_CLEAR` or call `karpatkit.cache.clear()`.


## Running the test

```
pip install -r requirements-dev.txt

pytest -vs tests/

```

## Building and distributing

```
pip install --upgrade build

python -m build

```


## Contributing

PRs are welcome!

Found a Bug ? Create an Issue.



## Development

If it's possible, just use `make` witch gives you many shortcuts.  Otherwise try to mimic what it does by seeing
[Makefile](Makefile).

The easy way is to call `make`, which by default build the docker image with all the dependencies and install the git
pre-commit hook to encorage you to commit well formatted code.


### Build the docker image

Run `make build` to build the docker image used to following development workflows.

The default image name used is `defyes`. You could override it specify `make build image=...`.

The default `CONFIG_FILE` is defined as `config.json` from the current working directory.

Every time a command is executed using this image, all the repository directory is mounted at `/repo` which is also
the default current working directory inside the container. `.tmp` is mounted to `/tmp`, where the Internet
requests/responces cache lives by default. `/repo/.home` is defined as the `HOME` to keep bash and ipython
configurations and history across shell sessions.


### Install the pre-commit hook

To install or re-install the pre-commit hook, call `make install-pre-commit`. It'll copy the [.pre-commit](.pre-commit)
file into the `.git` directory, to check for [linting](#linting) every time you try to create a new git
commit.


### Linting

Linting is the process to check code format accomplishment.

From now on you shoud ensure linting before commiting code. To help you doing that, `make lint` just check the code
formatting.  It includes executing `black`, `isort` and `flake8` just in checking mode. If you want to apply `black`
and `isort` changes automatically to your working-copy code, use `make pretty`.

`flake8` just check the code, but it doesn't apply chages automatically. You shoud decide how to make the changes
yourself base on the `flake8` output. Anyway, many code formatting rules `flake8` checks are sanitized automatically
by `black`.

> To change the default path where the linter checks, you could specify `make lint path=...`.


### Testing

The short way is just calling `make test`, which runs all tests.

if you want to specify a non default `config.json`, just overrider the env like
```shell
make test CONFIG_FILE=...
```

To have more control see [below](#a-shell-inside-the-container).


### IPython

Run `make ipython` straight away or `make shell` and then `ipython`.


### A shell inside the container

If you prefer to have more control over linting, testing, or debugging, execute `make shell`.

`make shell` starts `bash` inside the container. Then, you can directly run `pytest`, `black`, `ipython`, etc.

`bash`, as well as `ipython`, keeps its command history ;)

`make shell` executes `bash` with the same user you called it (your own user). As the repo volume is mounted in
read-write mode inside the container, it's useful to have new files or modified files with the same user you own
instead of the root user. But, if you prefer to run it with the root user, call `make rootshell` instead.

> `make` is always intended to be used outside the container.

Some examples of calling `pytest` inside the container could be:

```shell
pytest -v
```
```shell
pytest -vvs tests/test_azuro.py
```
```shell
pytest tests/test_azuro.py --pdb -k deposit
```

> The `.home` directory is git ignored to prevent committing command history among other things, except for the
> `.home/.bashrc` which you can edit and commit changes on it to define new bash command aliases or change the prompt.

