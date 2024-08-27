# hatch-deps-selector

[![PyPI - Version](https://img.shields.io/pypi/v/hatch-deps-selector.svg)](https://pypi.org/project/hatch-deps-selector)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-deps-selector.svg)](https://pypi.org/project/hatch-deps-selector)

-----

This package provides a Hatch plugin for configuring "variants" of dependencies according to an environment variable.
This can be used e.g. to change the package dependencies for conda-forge vs PyPI builds.

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Global dependency

Ensure `hatch-deps-selector` is defined within the `build-system.requires` field in your `pyproject.toml` file.

```toml
[build-system]
requires = ["hatchling", "hatch-deps-selector"]
build-backend = "hatchling.build"
```

## Build plugin

The [build plugin](https://hatch.pypa.io/latest/plugins/build-hook/reference/) name is `selector`.

- ***pyproject.toml***

    ```toml
    [tool.hatch.build.hooks.selector]
    env-var = <ENV-VAR-NAME>
    
    [tool.hatch.build.hooks.selector.variants.<VARIANT>]
    dependencies = ["numpy"]
    ```

- ***hatch.toml***

    ```toml
    [build.hooks.selector.variants.PYPI]
    dependencies = ["numpy"]
    ```

By default, set `HATCH_SELECTOR_VARIANT=<VARIANT>` to select the dependencies from `<VARIANT>` as additional project dependencies.
This might be used to only pull in certain dependencies when building for PyPI vs conda-forge.


### Build plugin options

| Option     | Type   | Default                  | Description                                            |
|------------|--------|--------------------------|--------------------------------------------------------|
| `env-var`  | `str`  | `HATCH_SELECTOR_VARIANT` | Name of environment variable to control built variant. |
| `variants` | `dict` | `{}`                     | Table of variant-tables with `dependencies` field.     |

## License

`hatch-deps-selector` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
