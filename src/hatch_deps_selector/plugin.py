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
        return self.__variants


    def initialize(self, version, build_data):
        # Allow variant to be unset or empty
        variant_name = os.environ.get(self.env_var)
        if not variant_name:
            return

        # But if defined, variant should exist in config
        try:
            variant = self.variants[variant_name]
        except KeyError:
            raise ValueError(f"Variant `{variant_name}` not found for build hook `{self.PLUGIN_NAME}`") from None

        # And variant should be a table
        if not isinstance(variant, dict):
            raise TypeError(f"Option `variants.{variant_name}` for build hook `{self.PLUGIN_NAME}` must be a table")
        # Dependencies do not need to be defined
        try:  
            dependencies = variant["dependencies"]
        except KeyError:
            raise ValueError(f"Option `dependencies` not found in table `variants.{variant_name}` for build hook `{self.PLUGIN_NAME}`") from None

        build_data["dependencies"].extend(dependencies)

