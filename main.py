import sys

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


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 900)
        self.setWindowTitle("Offline AI Translator")
        self.setWindowIcon(QIcon("misc/logo/icon.png"))
        self.source_textarea: str = None
        self.target_textarea: str = None
        self.languages: dict[str, str] = {
            "English": "en",
            "Deutsch": "de",
        }
        self.source_combobox = QComboBox()
        self.target_combobox = QComboBox()

        layout = QGridLayout()

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

        self.source_textarea = QTextEdit()
        self.source_textarea.setText("")
        layout.addWidget(self.source_textarea, 1, 0)

        self.target_textarea = QTextEdit()
        self.target_textarea.setText("")
        layout.addWidget(self.target_textarea, 1, 1)

        btn_translate = QPushButton()
        btn_translate.setText("Translate")
        layout.addWidget(btn_translate, 2, 0, 2, 2)
        btn_translate.clicked.connect(
            lambda: self.translate(
                self.languages[self.source_combobox.currentText()],
                self.languages[self.target_combobox.currentText()],
                self.source_textarea.toPlainText(),
            )
        )

        self.clear_button(
            layout, self.source_textarea, 1, 0, (Qt.AlignTop | Qt.AlignRight)
        )
        self.clear_button(
            layout, self.target_textarea, 1, 1, (Qt.AlignTop | Qt.AlignRight)
        )

        self.setLayout(layout)

    def clear_button(
        self, layout: any, textarea: any, row: int, column: int, alignment: int
    ) -> None:
        clear_icon = qta.icon("fa5.times-circle")
        clear_button = QPushButton(clear_icon, "")
        layout.addWidget(clear_button, row, column, alignment=(alignment))
        size_clear_button = QSize(30, 30)
        clear_button.setFixedSize(size_clear_button)
        clear_button.clicked.connect(lambda: textarea.setText(""))

    def lang_swap(self, value) -> str:
        for item in self.languages:
            if self.languages[item] != value:
                return item

    def switch_lang_on_change(self, value: str) -> None:
        self.target_combobox.setCurrentText(self.lang_swap(value))

    def translate(self, src_lang: str, trg_lang: str, text: str) -> None:
        translated_text = Translator(src_lang, trg_lang, text).set_translate()
        self.target_textarea.setText(translated_text)


app = QApplication(sys.argv)
main_window = Main()
main_window.show()
sys.exit(app.exec())
