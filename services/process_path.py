from pathlib import Path

from services.process_book import process_book


def process_path(folder_path):
    from handlers.comands import send_telegram_message

    folder = Path(folder_path)

    if not folder.exists():
        send_telegram_message(text=f"Путь '{folder_path}' не существует.")
        return
    if not folder.is_dir():
        send_telegram_message(text=f"'{folder_path}' не является папкой.")
        return

    for item in folder.iterdir():
        try:
            # Если элемент является файлом и имеет расширение .pdf
            if item.is_file():
                if item.suffix.lower() == ".pdf":
                    process_book(str(item.resolve()))
            # Если элемент является папкой, рекурсивно обрабатываем её
            elif item.is_dir():
                process_path(item)
        except PermissionError:
            # Пропускаем элементы, доступ к которым запрещён
            send_telegram_message(f"Нет доступа к элементу: {item}")
            continue
