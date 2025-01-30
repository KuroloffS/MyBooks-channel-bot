import csv
from pathlib import Path

log_file_path = Path("send_logs.csv")


def initialize_log_file():
    if not log_file_path.exists():
        with open(log_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "BookName", "Success", "Error"])


def get_next_book_id():
    if log_file_path.exists():
        with open(log_file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) > 1:
                last_id = int(rows[-1][0])
                return last_id + 1
    return 1


def log_to_file(book_name, success, error=None):
    book_id = get_next_book_id()

    with open(log_file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([book_id, book_name, success, error])


initialize_log_file()
