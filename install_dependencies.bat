@echo off
:: Устанавливаем кодировку для вывода сообщений в консоль
chcp 65001

echo Установка зависимостей для OCR Translator...

:: Устанавливаем необходимые Python библиотеки
echo Устанавливаем необходимые Python библиотеки...
pip install googletrans==4.0.0-rc1 pytesseract PyQt5 Pillow

:: Проверка наличия Tesseract OCR
echo Проверка наличия Tesseract OCR...
where tesseract >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo Tesseract не найден. Пожалуйста, установите Tesseract OCR с https://github.com/tesseract-ocr/tesseract
    echo.
    pause
    exit /b
)

:: Настройка переменной окружения для Tesseract (если требуется)
set TESSERACT_PATH="C:\Program Files\Tesseract-OCR\tesseract.exe"
if not exist %TESSERACT_PATH% (
    echo.
    echo Указанный путь к Tesseract не найден.
    echo Пожалуйста, установите Tesseract OCR с https://github.com/tesseract-ocr/tesseract
    echo После установки укажите правильный путь в скрипте или настройте переменную окружения.
    pause
    exit /b
)

:: Подтверждение успешной установки
echo.
echo Все зависимости успешно установлены.
echo Вы можете запустить приложение.
pause
