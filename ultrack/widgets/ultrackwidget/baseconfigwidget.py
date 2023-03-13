import logging
from abc import abstractmethod
from typing import Any, Dict, Optional

from magicgui.widgets import Container, Label
from pydantic import BaseModel
from toolz import curry

LOG = logging.getLogger(__name__)


class BaseConfigWidget(Container):
    def __init__(self, config: BaseModel, label: Optional[str] = None):
        super().__init__()

        if label is not None:
            self.append(Label(label=label))

        self._attr_to_widget: Dict[str, Container] = {}
        self._setup_widgets()
        self.config = config

        self.native.layout().addStretch(0)

    @abstractmethod
    def _setup_widgets(self) -> None:
        pass

    @property
    def config(self) -> BaseModel:
        return self._config

    @config.setter
    def config(self, value: BaseModel) -> None:
        """Sets config and updates the sub widgets values"""
        self._config = value
        for k, v in self._config:
            # some parameters might not be exposed in the UI
            if k in self._attr_to_widget:
                widget = self._attr_to_widget[k]
                widget.changed.disconnect()
                widget.value = v
                widget.changed.connect(self.set_config(k))

    @curry
    def set_config(self, key: str, value: Any) -> None:
        """Updates config attribute and logs it"""
        LOG.info(f"Updating {type(self).__name__} {key} with value {value}")
        setattr(self._config, key, value)
