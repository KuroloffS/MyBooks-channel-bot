import os
from pdf2image import convert_from_path
from tempfile import TemporaryDirectory


def process_book(pdf_path: str, dpi: int = 200) -> tuple[bytes, str]:
    from handlers.comands import (
        send_telegram_message,
        send_telegram_photo,
        send_reply_channel_message,
    )

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Файл не найден: {pdf_path}")
    if not os.path.isfile(pdf_path):
        raise ValueError(f"Путь не является файлом: {pdf_path}")

    # Временная директория для сохранения изображений
    with TemporaryDirectory() as temp_dir:
        try:
            # Конвертируем первую страницу в PNG
            images = convert_from_path(
                pdf_path=pdf_path,
                dpi=dpi,
                first_page=1,  # Нумерация с 1
                last_page=1,
                output_folder=temp_dir,
                fmt="png",
                paths_only=True,
                poppler_path=r"D:\poppler-24.08.0\Library\bin",
            )

            # Если изображений нет → ошибка
            if not images:
                raise RuntimeError("Не удалось извлечь страницы PDF")

            # Читаем первое изображение как байты
            with open(images[0], "rb") as f:
                image_bytes = f.read()

            message_id = send_telegram_photo(photo=image_bytes)
            send_telegram_message = send_reply_channel_message(
                document_path=pdf_path, reply_to_message_id=message_id
            )

        except Exception as e:
            raise RuntimeError(f"Ошибка обработки PDF: {str(e)}")
