# SPDX-FileCopyrightText: 2022-present Angus Hollands <goosey15@gmail.com>
#
# SPDX-License-Identifier: MIT
from hatchling.plugin import hookimpl

from .plugin import DependenciesSelectorHook


@hookimpl
def hatch_register_build_hook():
    return DependenciesSelectorHook

