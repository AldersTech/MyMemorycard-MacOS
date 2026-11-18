"""The application icon, drawn rather than shipped.

The original carried 2004-era Windows ``.ico`` blobs base64 encoded in a
Python source file; at 32x32 they look rough on a Retina display.  These
are drawn with QPainter instead, so they stay sharp at any size.
"""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)

_CARD_BODY = QColor("#3b4252")
_CARD_EDGE = QColor("#1f232b")
_CARD_TOP = QColor("#5a6683")
_LABEL = QColor("#e8ecf5")
_ACCENT = QColor("#4c8dff")


def _draw_card(painter: QPainter, size: int):
    """Draw a PS2 memory card silhouette filling a size x size box."""
    s = size
    painter.setRenderHint(QPainter.Antialiasing, True)

    body = QRectF(s * 0.17, s * 0.09, s * 0.66, s * 0.82)
    radius = s * 0.09

    path = QPainterPath()
    path.addRoundedRect(body, radius, radius)

    gradient = QLinearGradient(body.topLeft(), body.bottomRight())
    gradient.setColorAt(0.0, _CARD_TOP)
    gradient.setColorAt(1.0, _CARD_BODY)
    painter.fillPath(path, QBrush(gradient))

    pen_width = max(1.0, s * 0.022)
    painter.setPen(QColor(_CARD_EDGE))
    painter.save()
    p = painter.pen()
    p.setWidthF(pen_width)
    painter.setPen(p)
    painter.drawPath(path)
    painter.restore()

    # the connector slot along the top edge
    connector = QRectF(s * 0.28, s * 0.14, s * 0.44, s * 0.11)
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor(_CARD_EDGE))
    painter.drawRoundedRect(connector, s * 0.02, s * 0.02)
    painter.setBrush(_ACCENT)
    for i in range(4):
        x = connector.left() + s * 0.035 + i * s * 0.105
        painter.drawRect(QRectF(x, connector.top() + s * 0.025, s * 0.05, s * 0.06))

    # the white label area
    label = QRectF(s * 0.25, s * 0.36, s * 0.50, s * 0.42)
    painter.setBrush(_LABEL)
    painter.drawRoundedRect(label, s * 0.035, s * 0.035)

    painter.setBrush(QColor("#98a2b8"))
    for i in range(3):
        y = label.top() + s * 0.09 + i * s * 0.11
        width = label.width() * (0.72 if i != 1 else 0.52)
        painter.drawRoundedRect(
            QRectF(label.left() + s * 0.06, y, width, s * 0.045), s * 0.02, s * 0.02
        )


def _rounded(rect, radius):
    path = QPainterPath()
    path.addRoundedRect(rect, radius, radius)
    return path


def draw_app_icon(painter: QPainter, size: int):
    """Draw the application icon filling a size x size box.

    It follows the macOS icon grid: a rounded tile inset about 10% from
    the edges, with a soft shadow.  On the tile sits a memory card, tilted
    slightly, with a grid of coloured save blocks on its label, and a
    badge with arrows going both ways for importing and exporting saves.
    """
    s = float(size)
    painter.save()
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setPen(Qt.NoPen)

    # --- the tile, with a soft drop shadow -------------------------------
    inset = s * 0.098
    tile = QRectF(inset, inset, s - 2 * inset, s - 2 * inset)
    radius = tile.width() * 0.225
    if s >= 64:
        steps = 10
        for i in range(steps):
            grow = s * 0.03 * (steps - i) / steps
            shadow = tile.adjusted(-grow * 0.6, -grow * 0.3 + s * 0.01,
                                   grow * 0.6, grow * 1.2 + s * 0.01)
            painter.setBrush(QColor(0, 0, 0, 9))
            painter.drawPath(_rounded(shadow, radius + grow * 0.6))

    tile_path = _rounded(tile, radius)
    bg = QLinearGradient(tile.topLeft(), tile.bottomRight())
    bg.setColorAt(0.0, QColor("#8e8e8e"))
    bg.setColorAt(0.55, QColor("#787878"))
    bg.setColorAt(1.0, QColor("#595959"))
    painter.fillPath(tile_path, QBrush(bg))

    # soft light from the top
    sheen = QLinearGradient(tile.topLeft(), tile.center())
    sheen.setColorAt(0.0, QColor(255, 255, 255, 46))
    sheen.setColorAt(1.0, QColor(255, 255, 255, 0))
    painter.fillPath(tile_path, QBrush(sheen))

    painter.setClipPath(tile_path)

    # --- the memory card --------------------------------------------------
    painter.save()
    painter.translate(s * 0.45, s * 0.47)
    painter.rotate(-9)
    cw, ch = s * 0.40, s * 0.50
    card = QRectF(-cw / 2, -ch / 2, cw, ch)

    # body: a rounded rectangle with the top corners cut at an angle
    cut = cw * 0.16
    r = s * 0.035
    body = QPainterPath()
    body.moveTo(card.left() + cut, card.top())
    body.lineTo(card.right() - cut, card.top())
    body.lineTo(card.right(), card.top() + cut)
    body.lineTo(card.right(), card.bottom() - r)
    body.quadTo(card.right(), card.bottom(), card.right() - r, card.bottom())
    body.lineTo(card.left() + r, card.bottom())
    body.quadTo(card.left(), card.bottom(), card.left(), card.bottom() - r)
    body.lineTo(card.left(), card.top() + cut)
    body.closeSubpath()

    # shadow under the card, the same shape as the card
    painter.fillPath(body.translated(s * 0.006, s * 0.022), QColor(0, 0, 0, 80))

    shell = QLinearGradient(card.topLeft(), card.bottomRight())
    shell.setColorAt(0.0, QColor("#3d4250"))
    shell.setColorAt(1.0, QColor("#15171d"))
    painter.fillPath(body, QBrush(shell))
    if s >= 32:
        edge = painter.pen()
        edge.setColor(QColor(255, 255, 255, 40))
        edge.setWidthF(max(1.0, s * 0.006))
        painter.strokePath(body, edge)

    # gold contacts along the top
    contacts = 6 if s >= 64 else 3
    band = QRectF(card.left() + cw * 0.20, card.top() + ch * 0.07,
                  cw * 0.60, ch * 0.10)
    painter.setBrush(QColor("#0d0e12"))
    painter.drawPath(_rounded(band, s * 0.012))
    gold = QLinearGradient(band.topLeft(), band.bottomLeft())
    gold.setColorAt(0.0, QColor("#ffe08a"))
    gold.setColorAt(1.0, QColor("#c98f1c"))
    painter.setBrush(QBrush(gold))
    gap = band.width() / contacts
    for i in range(contacts):
        pin = QRectF(band.left() + gap * i + gap * 0.22, band.top() + band.height() * 0.2,
                     gap * 0.56, band.height() * 0.6)
        painter.drawRect(pin)

    # the label, holding a 2x2 grid of saves
    label = QRectF(card.left() + cw * 0.12, card.top() + ch * 0.27,
                   cw * 0.76, ch * 0.62)
    painter.setBrush(QColor("#f1f3fa"))
    painter.drawPath(_rounded(label, s * 0.025))

    pad = label.width() * 0.10
    cell = (label.width() - pad * 3) / 2
    top = label.top() + (label.height() - (cell * 2 + pad)) / 2
    for i, (a, b) in enumerate((("#22d3ee", "#0891b2"), ("#f472b6", "#db2777"),
                                ("#fbbf24", "#ea580c"), ("#4ade80", "#16a34a"))):
        x = label.left() + pad + (i % 2) * (cell + pad)
        y = top + (i // 2) * (cell + pad)
        block = QRectF(x, y, cell, cell)
        fill = QLinearGradient(block.topLeft(), block.bottomRight())
        fill.setColorAt(0.0, QColor(a))
        fill.setColorAt(1.0, QColor(b))
        painter.setBrush(QBrush(fill))
        painter.drawPath(_rounded(block, cell * 0.22))
    painter.restore()

    # --- the import / export badge ---------------------------------------
    centre_x, centre_y, br = s * 0.70, s * 0.70, s * 0.125
    painter.setBrush(QColor("#141743"))
    painter.drawEllipse(QPointF(centre_x, centre_y), br * 1.12, br * 1.12)
    badge = QLinearGradient(centre_x - br, centre_y - br, centre_x + br, centre_y + br)
    badge.setColorAt(0.0, QColor("#3883ff"))
    badge.setColorAt(1.0, QColor("#1e56e4"))
    painter.setBrush(QBrush(badge))
    painter.drawEllipse(QPointF(centre_x, centre_y), br, br)

    pen = QPen(QColor("white"))
    pen.setWidthF(max(1.0, s * 0.022))
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)
    span, head, dx = br * 0.52, br * 0.26, br * 0.30
    # up arrow on the left, down arrow on the right
    ux, dxr = centre_x - dx, centre_x + dx
    painter.drawLine(QPointF(ux, centre_y + span), QPointF(ux, centre_y - span))
    painter.drawLine(QPointF(ux - head, centre_y - span + head), QPointF(ux, centre_y - span))
    painter.drawLine(QPointF(ux + head, centre_y - span + head), QPointF(ux, centre_y - span))
    painter.drawLine(QPointF(dxr, centre_y - span), QPointF(dxr, centre_y + span))
    painter.drawLine(QPointF(dxr - head, centre_y + span - head), QPointF(dxr, centre_y + span))
    painter.drawLine(QPointF(dxr + head, centre_y + span - head), QPointF(dxr, centre_y + span))

    painter.restore()


def app_icon() -> QIcon:
    """Build the multi-resolution application icon."""
    icon = QIcon()
    for size in (16, 32, 64, 128, 256, 512, 1024):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        draw_app_icon(painter, size)
        painter.end()
        icon.addPixmap(pixmap)
    return icon


def _glyph(size: int, draw) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing, True)
    draw(painter, size)
    painter.end()
    return pixmap


def _arrow(painter, size, up, color):
    s = size
    pen = painter.pen()
    pen.setColor(color)
    pen.setWidthF(max(1.6, s * 0.11))
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    painter.setPen(pen)

    cx = s * 0.5
    top, bottom = s * 0.20, s * 0.66
    painter.drawLine(cx, top if up else bottom, cx, bottom if up else top)
    head = s * 0.17
    tip_y = top if up else bottom
    dy = head if up else -head
    painter.drawLine(cx - head, tip_y + dy, cx, tip_y)
    painter.drawLine(cx + head, tip_y + dy, cx, tip_y)
    painter.drawLine(s * 0.16, s * 0.84, s * 0.84, s * 0.84)


def toolbar_icons(color: QColor) -> dict:
    """Simple monochrome toolbar glyphs that follow the current theme."""

    def open_card(painter, s):
        # A memory card outline, drawn with the same pen as the others.
        pen = QPen(color)
        pen.setWidthF(max(1.6, s * 0.10))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        left, right, top, bottom = s * 0.22, s * 0.78, s * 0.14, s * 0.86
        cut, r = s * 0.14, s * 0.07
        outline = QPainterPath()
        outline.moveTo(left + r, top)
        outline.lineTo(right - cut, top)
        outline.lineTo(right, top + cut)
        outline.lineTo(right, bottom - r)
        outline.quadTo(right, bottom, right - r, bottom)
        outline.lineTo(left + r, bottom)
        outline.quadTo(left, bottom, left, bottom - r)
        outline.lineTo(left, top + r)
        outline.quadTo(left, top, left + r, top)
        painter.drawPath(outline)
        # contacts along the top
        for x in (0.37, 0.50):
            painter.drawLine(QPointF(s * x, s * 0.30), QPointF(s * x, s * 0.40))
        # the label
        painter.drawLine(QPointF(s * 0.36, s * 0.58), QPointF(s * 0.64, s * 0.58))
        painter.drawLine(QPointF(s * 0.36, s * 0.71), QPointF(s * 0.56, s * 0.71))

    def import_glyph(painter, s):
        _arrow(painter, s, False, color)

    def export_glyph(painter, s):
        _arrow(painter, s, True, color)

    def delete_glyph(painter, s):
        pen = painter.pen()
        pen.setColor(color)
        pen.setWidthF(max(1.6, s * 0.10))
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(s * 0.20, s * 0.28, s * 0.80, s * 0.28)
        painter.drawLine(s * 0.40, s * 0.28, s * 0.42, s * 0.18)
        painter.drawLine(s * 0.60, s * 0.28, s * 0.58, s * 0.18)
        painter.drawLine(s * 0.42, s * 0.18, s * 0.58, s * 0.18)
        painter.drawLine(s * 0.27, s * 0.28, s * 0.32, s * 0.82)
        painter.drawLine(s * 0.73, s * 0.28, s * 0.68, s * 0.82)
        painter.drawLine(s * 0.32, s * 0.82, s * 0.68, s * 0.82)

    return {
        name: QIcon(_glyph(64, fn))
        for name, fn in (
            ("open", open_card),
            ("import", import_glyph),
            ("export", export_glyph),
            ("delete", delete_glyph),
        )
    }
