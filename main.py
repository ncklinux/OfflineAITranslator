import sys
import os
from typing import Any

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QWidget,
    QTextEdit,
    QPushButton,
    QComboBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import qtawesome as qta

from common.translator import Translator

# Determine the base path for resource files
# If running as a PyInstaller bundle (frozen), use the temporary extraction folder (sys._MEIPASS)
# Otherwise, use the directory containing the current script
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# For opus-mt-en-de and opus-mt-de-en lang models
model_dir_en_de = os.path.join(base_path, "language_models", "opus-mt-en-de")
model_dir_de_en = os.path.join(base_path, "language_models", "opus-mt-de-en")


class Main(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1600, 900)
        self.setWindowTitle("Offline AI Translator")
        self.setWindowIcon(QIcon("misc/logo/icon.png"))
        self.source_textarea: Any = None
        self.target_textarea: Any = None
        self.languages: dict[str, str] = {
            "English": "en",
            "Deutsch": "de",
        }
        self.source_combobox = QComboBox()
        self.target_combobox = QComboBox()

        layout = QGridLayout()

        # Language selection
        for item in self.languages:
            self.source_combobox.addItem(item)
        layout.addWidget(self.source_combobox, 0, 0)
        self.source_combobox.currentTextChanged.connect(
            lambda: self.switch_lang_on_change(
                self.languages[self.source_combobox.currentText()]
            )
        )

        for item in self.languages:
            self.target_combobox.addItem(item)
        self.target_combobox.setCurrentText(
            self.lang_swap(self.languages[self.target_combobox.currentText()])
        )
        layout.addWidget(self.target_combobox, 0, 1)

        # Switch language button
        self.btn_switch_lang = QPushButton("Switch Languages")
        layout.addWidget(self.btn_switch_lang, 1, 0, 1, 2)
        self.btn_switch_lang.clicked.connect(self.switch_languages)

        # Source text area with clear button
        source_container, self.source_textarea = (
            self.create_textarea_with_clear_button()
        )
        layout.addWidget(source_container, 2, 0)

        # Target text area with clear button
        target_container, self.target_textarea = (
            self.create_textarea_with_clear_button()
        )
        layout.addWidget(target_container, 2, 1)

        # Translate button (changed from local to instance variable)
        self.btn_translate = QPushButton()
        self.btn_translate.setText("Translate")
        layout.addWidget(self.btn_translate, 3, 0, 1, 2)
        self.btn_translate.clicked.connect(
            lambda: self.translate(
                self.languages[self.source_combobox.currentText()],
                self.languages[self.target_combobox.currentText()],
                self.source_textarea.toPlainText(),
            )
        )
        self.btn_translate.setFixedHeight(60)  # Set height in pixels
        self.btn_translate.setEnabled(False)  # Disabled by default

        # Connect signal to enable/disable translate button
        self.source_textarea.textChanged.connect(self.update_translate_button_state)

        self.setLayout(layout)

    def create_textarea_with_clear_button(self) -> tuple[QWidget, QTextEdit]:
        container = QWidget()
        layout = QGridLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        textarea = QTextEdit()
        clear_icon = qta.icon("fa5.times-circle")
        clear_button = QPushButton(clear_icon, "")
        clear_button.setFixedSize(QSize(24, 24))
        clear_button.setToolTip("Clear text")
        clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        # clear_button.setFlat(True)  # Optional

        # Add clear button to layout (row 0, col 1), aligned top-right
        layout.addWidget(
            clear_button,
            0,
            1,
            alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
        )

        # Set minimum height for row 1 (adds space below clear button)
        layout.setRowMinimumHeight(1, 6)  # Pixels of space after the clear button

        # Add textarea to layout (row 2, col 0, spanning 1 row and 2 columns)
        layout.addWidget(textarea, 2, 0, 1, 2)

        clear_button.clicked.connect(lambda: textarea.clear())

        return container, textarea

    def update_translate_button_state(self) -> None:
        text = self.source_textarea.toPlainText().strip()
        self.btn_translate.setEnabled(bool(text))

    def lang_swap(self, value) -> str:
        for item in self.languages:
            if self.languages[item] != value:
                return item

    def switch_languages(self) -> None:
        src_index = self.source_combobox.currentIndex()
        trg_index = self.target_combobox.currentIndex()
        self.source_combobox.setCurrentIndex(trg_index)
        self.target_combobox.setCurrentIndex(src_index)

    def switch_lang_on_change(self, value: str) -> None:
        self.target_combobox.setCurrentText(self.lang_swap(value))

    def translate(self, src_lang: str, trg_lang: str, text: str) -> None:
        translated_text = Translator(src_lang, trg_lang, text).set_translate()
        self.target_textarea.setText(translated_text)


app = QApplication(sys.argv)
main_window = Main()
main_window.show()
sys.exit(app.exec())
