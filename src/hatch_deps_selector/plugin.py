import os
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class DependenciesSelectorHook(BuildHookInterface):
    PLUGIN_NAME = "selector"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__env_var = None
        self.__variants = None

    @property
    def env_var(self):
        if self.__env_var is None:
            env_var = self.config.get("env-var", "HATCH_SELECTOR_VARIANT")
            if not isinstance(env_var, str):
                raise TypeError(f"Option `env-var` for build hook `{self.PLUGIN_NAME}` must be a string")

            self.__env_var = env_var
        return self.__env_var

    @property
    def variants(self):
        if self.__variants is None:
            variants = self.config.get("variants", {})
            if not isinstance(variants, dict):
                raise TypeError(f"Option `variants` for build hook `{self.PLUGIN_NAME}` must be a table")

            self.__variants = variants
        return self.variants


    def initialize(self, version, build_data):
        # Allow variant to be unset or empty
        variant = os.environ.get(self.env_var)
        if not variant:
            return

        # But if defined, should be valid
        dependencies = self.variants.get(variant, [])
        if dependencies is None:
            raise ValueError(f"Variant `{variant}` not found for build hook `{self.PLUGIN_NAME}`")
        build_data["dependencies"].extend(dependencies)

