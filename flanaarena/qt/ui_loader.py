from collections.abc import Iterable

from PySide6 import QtCore, QtUiTools, QtWidgets


class UiLoader(QtUiTools.QUiLoader):
    def __init__(
        self,
        base_instance: QtWidgets.QWidget | None,
        custom_widgets: Iterable[type[QtWidgets.QWidget]] = ()
    ) -> None:
        super().__init__(base_instance)
        self._base_instance = base_instance

        for widget_class in custom_widgets:
            self.registerCustomWidget(widget_class)

    def createWidget(self, class_name: str, parent: QtCore.QObject | None = None, name: str = '') -> QtWidgets.QWidget:
        if not parent and self._base_instance:
            return self._base_instance

        widget = super().createWidget(class_name, parent, name)

        if self._base_instance and name:
            setattr(self._base_instance, name, widget)

        return widget
