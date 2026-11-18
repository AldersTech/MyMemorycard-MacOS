"""Colours and the style sheet that give mymc its look.

Two palettes, light and dark, follow the system appearance.  The accent
colour comes from the system too, so it matches whatever the user picked
in System Settings.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QGuiApplication, QPalette


def is_dark():
    hints = QGuiApplication.styleHints()
    scheme = getattr(hints, "colorScheme", lambda: Qt.ColorScheme.Unknown)()
    if scheme == Qt.ColorScheme.Dark:
        return True
    if scheme == Qt.ColorScheme.Light:
        return False
    return QGuiApplication.palette().color(QPalette.Window).lightness() < 128


def accent_color():
    palette = QGuiApplication.palette()
    role = getattr(QPalette, "Accent", QPalette.Highlight)
    color = palette.color(role)
    if not color.isValid() or color.saturation() < 40:
        color = QColor("#0a84ff")
    return color


def colors():
    """The current set of named colours, as QColors."""
    accent = accent_color()
    if is_dark():
        c = {
            "window": "#1c1c1e",
            "panel": "#232326",
            "stage": "#2c2c30",
            "border": "#38383c",
            "text": "#f2f2f7",
            "muted": "#98989f",
            "hover": "#2f2f33",
            "field": "#2c2c30",
            "track": "#3a3a3e",
            "warn": "#ff9f0a",
        }
        sel_alpha = 0.32
    else:
        c = {
            "window": "#ffffff",
            "panel": "#f5f5f7",
            "stage": "#e9e9ee",
            "border": "#e1e1e6",
            "text": "#1d1d1f",
            "muted": "#6e6e73",
            "hover": "#ececf0",
            "field": "#ffffff",
            "track": "#dcdce1",
            "warn": "#ff9500",
        }
        sel_alpha = 0.18
    c = {k: QColor(v) for k, v in c.items()}
    c["accent"] = accent
    selection = QColor(accent)
    selection.setAlphaF(sel_alpha)
    c["selection"] = selection
    c["accent_hover"] = accent.lighter(112)
    return c


def _rgba(color):
    return "rgba(%d, %d, %d, %.3f)" % (
        color.red(), color.green(), color.blue(), color.alphaF()
    )


def stylesheet(c):
    v = {k: _rgba(col) for k, col in c.items()}
    return """
    QMainWindow, QWidget#central {{ background: {window}; }}

    QToolBar#mainToolbar {{
        background: {window};
        border: none;
        border-bottom: 1px solid {border};
        padding: 8px 10px;
        spacing: 4px;
    }}
    QToolBar#mainToolbar::separator {{
        background: {border};
        width: 1px;
        margin: 6px 6px;
    }}
    QToolBar#mainToolbar QToolButton {{
        color: {text};
        background: transparent;
        border: none;
        border-radius: 7px;
        padding: 5px 10px;
        font-weight: 500;
    }}
    QToolBar#mainToolbar QToolButton:hover {{ background: {hover}; }}
    QToolBar#mainToolbar QToolButton:pressed {{ background: {stage}; }}
    QToolBar#mainToolbar QToolButton:disabled {{ color: {muted}; }}
    QToolBar#mainToolbar QToolButton[popupMode="1"] {{ padding-right: 38px; }}
    QToolBar#mainToolbar QToolButton::menu-button {{
        border: none;
        width: 38px;
    }}
    QToolBar#mainToolbar QToolButton::menu-arrow {{
        width: 10px;
        height: 10px;
        subcontrol-position: center;
    }}

    QLineEdit#filter {{
        background: {field};
        color: {text};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 5px 10px;
        min-width: 200px;
        selection-background-color: {accent};
    }}
    QLineEdit#filter:focus {{ border: 1px solid {accent}; }}

    QTableWidget#saves {{
        background: {window};
        color: {text};
        border: none;
        outline: none;
        selection-background-color: {selection};
        selection-color: {text};
    }}
    QTableWidget#saves::item {{
        border: none;
        border-bottom: 1px solid {border};
        padding: 0 10px;
    }}
    QTableWidget#saves::item:hover {{ background: {hover}; }}
    QTableWidget#saves::item:selected {{
        background: {selection};
        color: {text};
    }}
    QHeaderView {{ background: {window}; border: none; }}
    QHeaderView::section {{
        background: {window};
        color: {muted};
        border: none;
        border-bottom: 1px solid {border};
        padding: 8px 10px;
        font-size: 11px;
        font-weight: 600;
    }}
    QHeaderView::section:hover {{ color: {text}; }}

    QLabel#emptyState {{ color: {muted}; font-size: 13px; }}
    QPushButton#primary, QPushButton#secondary {{
        border-radius: 8px;
        padding: 7px 16px;
        font-weight: 600;
        min-width: 90px;
    }}
    QPushButton#primary {{
        background: {accent};
        color: white;
        border: none;
    }}
    QPushButton#primary:hover {{ background: {accent_hover}; }}
    QPushButton#secondary {{
        background: {field};
        color: {text};
        border: 1px solid {border};
    }}
    QPushButton#secondary:hover {{ background: {hover}; }}

    QWidget#sidePanel {{
        background: {panel};
        border-left: 1px solid {border};
    }}
    QLabel#saveTitle {{
        color: {text};
        font-size: 18px;
        font-weight: 600;
    }}
    QLabel#saveSubtitle {{ color: {muted}; font-size: 12px; }}
    QLabel#detailKey {{ color: {muted}; font-size: 12px; }}
    QLabel#detailValue {{ color: {text}; font-size: 13px; }}
    QFrame#detailRule {{ background: {border}; max-height: 1px; border: none; }}

    QSplitter::handle {{ background: {border}; }}
    QSplitter::handle:horizontal {{ width: 1px; }}

    QStatusBar {{
        background: {window};
        color: {muted};
        border-top: 1px solid {border};
    }}
    QStatusBar::item {{ border: none; }}
    QStatusBar QLabel {{ color: {muted}; padding: 0 6px; }}
    QProgressBar#freeBar {{
        background: {track};
        border: none;
        border-radius: 3px;
        max-height: 6px;
        min-height: 6px;
    }}
    QProgressBar#freeBar::chunk {{
        background: {accent};
        border-radius: 3px;
    }}
    QProgressBar#freeBar[full="true"]::chunk {{ background: {warn}; }}

    QScrollBar:vertical {{
        background: transparent; width: 10px; margin: 2px;
    }}
    QScrollBar::handle:vertical {{
        background: {track}; border-radius: 3px; min-height: 30px;
    }}
    QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
    QScrollBar::add-page, QScrollBar::sub-page {{ background: none; }}
    """.format(**v)
