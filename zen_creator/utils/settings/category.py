from abc import ABC

from zen_creator.utils.config._base import Subscriptable
from zen_creator.utils.registry import Registry


class SettingsCategory(ABC, Subscriptable, Registry["SettingsCategory"], is_base_registry=True):
    """Base class for a named, type-checked group of settings.

    ZEN-creator defines no concrete settings categories itself. Downstream
    projects (e.g. ZEN-europe) define concrete subclasses with a unique
    ``name`` (e.g. ``"time_settings"``) and their own typed fields. Every
    registered subclass becomes queryable on ``Settings`` as
    ``model.settings.<name>``.
    """

    name: str = "generic_settings_category"
