from PySide6 import QtCore, QtGui, QtSvg

import constants


def create_qt_color(color: str) -> QtGui.QColor:
    if color.startswith('#') and len(color) == 9:
        qt_color = QtGui.QColor(color[:-2])
        qt_color.setAlpha(int(color[-2:], 16))
    else:
        qt_color = QtGui.QColor(color)

    return qt_color


def draw_mission_indicators(image: QtGui.QPixmap, missions_count: int) -> None:
    with QtGui.QPainter(image) as painter:
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        width = image.width()
        height = image.height()

        squares = 3
        margin = 4
        spacing = 2
        square_width = (width - 2 * margin - (squares - 1) * spacing) // squares
        square_height = 10

        y = height - square_height - margin

        for i in range(squares):
            x = margin + i * (square_width + spacing)
            rect = QtCore.QRect(x, y, square_width, square_height)

            if i < missions_count:
                painter.fillRect(rect, create_qt_color(constants.MISSION_RECT_INCOMPLETE_COLOR))
            else:
                painter.fillRect(rect, create_qt_color(constants.MISSION_RECT_COMPLETE_COLOR))

        if missions_count == 3:
            renderer = QtSvg.QSvgRenderer(str(constants.TICK_PATH))
            tick_size = min(width, height) // 2
            x = (width - tick_size) // 2
            y = (height - tick_size) // 2
            renderer.render(painter, QtCore.QRect(x, y, tick_size, tick_size))
