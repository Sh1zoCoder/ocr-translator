import sys
import pytesseract
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
                             QComboBox, QPushButton, QFileDialog, QHBoxLayout, QTextEdit)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image, ImageGrab
from googletrans import Translator


def extract_text_from_image(image, lang="eng"):
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        return f"Ошибка извлечения текста: {str(e)}"


def translate_text(text, source_language, target_language):
    try:
        translator = Translator()
        translated = translator.translate(text, src=source_language, dest=target_language)
        return translated.text
    except Exception as e:
        return f"Ошибка перевода: {str(e)}"


class OCRTranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Translator")
        self.setGeometry(100, 100, 700, 600)

        self.init_ui()

    def init_ui(self):
        # Тёмная тема
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #6c4cc8;
                color: #ffffff;
                font-size: 14px;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #5a3bb0;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #ffffff;
                font-size: 14px;
                border: 1px solid #6c4cc8;
                border-radius: 5px;
                padding: 5px;
            }
            QTextEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                font-size: 14px;
                border: 1px solid #6c4cc8;
                border-radius: 5px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Превью изображения
        self.image_label = QLabel("Предпросмотр изображения")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(600, 200)
        self.image_label.setStyleSheet("border: 2px solid gray; background-color: #3c3c3c;")
        layout.addWidget(self.image_label)

        # Кнопки выбора изображения
        button_layout = QHBoxLayout()

        self.paste_button = QPushButton("Вставить скриншот")
        self.paste_button.clicked.connect(self.paste_screenshot)
        button_layout.addWidget(self.paste_button)

        self.open_button = QPushButton("Открыть изображение")
        self.open_button.clicked.connect(self.open_image)
        button_layout.addWidget(self.open_button)

        layout.addLayout(button_layout)

        # Выбор языков
        source_language_layout = QHBoxLayout()
        source_language_label = QLabel("Язык исходного текста:")
        self.source_language_selector = QComboBox()
        self.source_language_selector.addItem("Русский", "rus")
        self.source_language_selector.addItem("Английский", "eng")
        self.source_language_selector.addItem("Испанский", "spa")
        self.source_language_selector.addItem("Французский", "fra")
        self.source_language_selector.addItem("Немецкий", "deu")
        self.source_language_selector.addItem("Китайский", "chi_sim")
        self.source_language_selector.addItem("Японский", "jpn")
        self.source_language_selector.addItem("Итальянский", "ita")
        self.source_language_selector.addItem("Арабский", "ara")
        self.source_language_selector.addItem("Хинди", "hin")
        self.source_language_selector.setCurrentIndex(1)  # По умолчанию английский
        source_language_layout.addWidget(source_language_label)
        source_language_layout.addWidget(self.source_language_selector)
        layout.addLayout(source_language_layout)

        target_language_layout = QHBoxLayout()
        target_language_label = QLabel("Перевести на язык:")
        self.target_language_selector = QComboBox()
        self.target_language_selector.addItem("Русский", "ru")
        self.target_language_selector.addItem("Английский", "en")
        self.target_language_selector.addItem("Испанский", "es")
        self.target_language_selector.addItem("Французский", "fr")
        self.target_language_selector.addItem("Немецкий", "de")
        self.target_language_selector.addItem("Китайский", "zh-cn")
        self.target_language_selector.addItem("Японский", "ja")
        self.target_language_selector.addItem("Итальянский", "it")
        self.target_language_selector.addItem("Арабский", "ar")
        self.target_language_selector.addItem("Хинди", "hi")
        self.target_language_selector.setCurrentIndex(0)  # По умолчанию русский
        target_language_layout.addWidget(target_language_label)
        target_language_layout.addWidget(self.target_language_selector)
        layout.addLayout(target_language_layout)

        # Кнопка перевода (в центре)
        self.translate_button = QPushButton("Перевести")
        self.translate_button.clicked.connect(self.translate_image_text)
        self.translate_button.setStyleSheet("""
            background-color: #8b5cf6;
            font-size: 16px;
            font-weight: bold;
            padding: 15px;
        """)
        layout.addWidget(self.translate_button, alignment=Qt.AlignCenter)

        # Поля вывода текста
        self.extracted_text_edit = QTextEdit()
        self.extracted_text_edit.setPlaceholderText("Извлеченный текст появится здесь...")
        self.extracted_text_edit.setReadOnly(True)
        layout.addWidget(self.extracted_text_edit)

        self.translated_text_edit = QTextEdit()
        self.translated_text_edit.setPlaceholderText("Переведенный текст появится здесь...")
        self.translated_text_edit.setReadOnly(True)
        layout.addWidget(self.translated_text_edit)

        central_widget.setLayout(layout)

        self.current_image = None
        self.extracted_text = ""
        self.translated_text = ""

    def paste_screenshot(self):
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                self.current_image = image.convert("RGB")
                self.display_image(self.current_image)
            else:
                self.show_error("Скриншот не найден в буфере обмена или формат не поддерживается.")
        except Exception as e:
            self.show_error(f"Ошибка: {str(e)}")

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть изображение", "", "Изображения (*.png *.jpg *.jpeg *.bmp *.tiff)", options=options)
        if file_path:
            try:
                image = Image.open(file_path).convert("RGB")
                self.current_image = image
                self.display_image(image)
            except Exception as e:
                self.show_error(f"Ошибка: {str(e)}")

    def translate_image_text(self):
        if self.current_image is None:
            self.show_error("Изображение не загружено.")
            return

        # Сопоставление языков pytesseract и googletrans
        LANGUAGE_CODES = {
            "rus": "ru",
            "eng": "en",
            "spa": "es",
            "fra": "fr",
            "deu": "de",
            "chi_sim": "zh-cn",
            "jpn": "ja",
            "ita": "it",
            "ara": "ar",
            "hin": "hi",
        }

        source_lang = self.source_language_selector.currentData()
        target_lang = self.target_language_selector.currentData()

        source_lang_google = LANGUAGE_CODES.get(source_lang)
        if not source_lang_google:
            self.show_error("Неподдерживаемый язык.")
            return

        self.extracted_text = extract_text_from_image(self.current_image, lang=source_lang)
        self.translated_text = translate_text(self.extracted_text, source_lang_google, target_lang)

        self.extracted_text_edit.setText(self.extracted_text)
        self.translated_text_edit.setText(self.translated_text)

    def display_image(self, image):
        try:
            image = image.convert("RGBA")
            data = image.tobytes("raw", "RGBA")
            qimage = QImage(data, image.width, image.height, QImage.Format_RGBA8888)

            pixmap = QPixmap.fromImage(qimage)
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        except Exception as e:
            self.show_error(f"Ошибка при отображении изображения: {str(e)}")

    def show_error(self, message):
        self.extracted_text_edit.setText("")
        self.translated_text_edit.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCRTranslatorApp()
    window.show()
    sys.exit(app.exec_())
