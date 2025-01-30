from pathlib import Path

from services.process_book import process_book
from services.convert import convert_to_pdf


def process_path(folder_path):
    from handlers.comands import send_telegram_message

    folder = Path(folder_path)

    if not folder.exists():
        send_telegram_message(text=f"Путь '{folder_path}' не существует.")
        return
    if not folder.is_dir():
        send_telegram_message(text=f"'{folder_path}' не является папкой.")
        return

    book_extensions = {".pdf", ".epub", ".mobi", ".djvu", ".fb2"}

    for item in folder.iterdir():
        try:
            if item.is_file() and item.suffix.lower() in book_extensions:
                convert_to_pdf(str(item.resolve()))
            elif item.is_dir():
                process_path(item)
        except PermissionError:
            send_telegram_message(f"Нет доступа к элементу: {item}")
            continue
