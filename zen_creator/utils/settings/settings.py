import importlib
from pathlib import Path
from typing import Any

from pydantic import ConfigDict, model_validator

from zen_creator.utils.config._base import Subscriptable

from .category import SettingsCategory


class Settings(Subscriptable):
    """Root settings container.

    Empty by default: concrete settings categories are registered by
    downstream projects as ``SettingsCategory`` subclasses (e.g.
    ZEN-europe's ``TimeSettings``, with ``name = "time_settings"``), and
    become queryable by name, e.g. ``model.settings.time_settings.<field>``.
    """

    model_config = ConfigDict(extra="allow", validate_assignment=True)

    @model_validator(mode="before")
    @classmethod
    def populate_and_validate_categories(cls, data: Any) -> Any:
        """Validate each registered category against its user-provided data.

        Every ``SettingsCategory`` subclass that has been imported (and
        therefore registered) is included in the result, using its own
        defaults unless the user provided an override for that category.
        """
        if not isinstance(data, dict):
            data = {}

        populated: dict[str, Any] = {}
        for name, category_cls in SettingsCategory.get_registry().items():
            if category_cls is SettingsCategory:
                continue
            populated[name] = category_cls.model_validate(data.get(name) or {})

        for key, value in data.items():
            if key not in populated:
                populated[key] = value

        return populated

    @classmethod
    def load_from_yaml(cls, path: str | Path) -> "Settings":
        if not isinstance(path, (str, Path)):
            raise TypeError(f"Expected path of type `str` or `Path`, got {type(path)}")

        config_path = Path(path)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Could not find the configuration file {config_path}."
            )

        yaml = importlib.import_module("yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            user_dict = yaml.safe_load(f) or {}

        return cls.model_validate(user_dict.get("settings") or {})
