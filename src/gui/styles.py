DARK_THEME = """
QMainWindow {
    background-color: #121212;
}

QWidget {
    color: #f1f1f1;
    font-family: "Segoe UI";
    font-size: 14px;
}

QLineEdit {
    background-color: #1e1e1e;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    padding: 12px;
}

QLineEdit:focus {
    border: 1px solid #8b5cf6;
}

QPushButton {
    background-color: #8b5cf6;
    border: none;
    border-radius: 8px;
    padding: 11px 18px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #9d72f7;
}

QPushButton:disabled {
    background-color: #3a3a3a;
    color: #777777;
}

QProgressBar {
    background-color: #1e1e1e;
    border: none;
    border-radius: 6px;
    height: 12px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #8b5cf6;
    border-radius: 6px;
}

QFrame#previewCard {
    background-color: #1b1b1b;
    border: 1px solid #303030;
    border-radius: 12px;
    padding: 12px;
}
"""