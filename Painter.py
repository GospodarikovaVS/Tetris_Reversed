from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame


class Painter(QFrame):
    def __init__(self, parent, row, col):
        super().__init__(parent)

        self.init_paint(row, col)

    def init_paint(self, row, col):
        self.BlockWidth = col
        self.BlockHeight = row
        self.field = []
        self.ColorScheme = ColorTables.Bright

    def square_width(self):
        return self.contentsRect().width() // self.BlockWidth

    def square_height(self):
        return self.contentsRect().height() // self.BlockHeight

    def refresh(self, field):
        self.field = field
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()

        field_top = rect.bottom() - self.BlockHeight * self.square_height()

        for i in range(self.BlockHeight):
            for j in range(self.BlockWidth):
                if self.field[i][j] != 0:
                    self.draw_square(painter,
                                     rect.left() + j * self.square_width(),
                                     field_top + i * self.square_height(), self.field[i][j])

    def draw_square(self, painter, x, y, shape):

        color = QColor(self.ColorScheme[shape - 1])
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.square_height() - 1, x, y)
        painter.drawLine(x, y, x + self.square_width() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.square_height() - 1,
                         x + self.square_width() - 1, y + self.square_height() - 1)
        painter.drawLine(x + self.square_width() - 1,
                         y + self.square_height() - 1, x + self.square_width() - 1, y + 1)


class ColorTables(object):
    # Difficulty: 0-4 blocks, 5 bomb, 6 stone, 7 unit  |+1, 0 - none
    Bright = [0xFF0700, 0xFFD200, 0x1531AE, 0x00C90D, 0x7109AA, 0x4D0600, 0x7E8A80, 0x02041A]
    Soft = [0xFF7673, 0xFFE673, 0x6F81D6, 0x67E46F, 0xAD66D5, 0x4D0600, 0x7E8A80, 0x02041A]
    Dark = [0xA60400, 0xA68800, 0x071A71, 0x008209, 0x48036F, 0x4D0600, 0x7E8A80, 0x02041A]
    Neon = [0xED0086, 0xFF9200, 0x66F9E9, 0xA6F900, 0x3600E3, 0x4D0600, 0x7E8A80, 0x02041A]
    Mono = [0xFFFFFF, 0xE3E3E3, 0xA6A5A5, 0x4F4F4E, 0x010101, 0x4D0600, 0x7E8A80, 0x02041A]
