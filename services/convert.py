from pathlib import Path
from config import CONVERT_API
from services.process_book import process_book
import convertapi


def convert_to_pdf(input_file_path):
    convertapi.api_credentials = CONVERT_API
    format = Path(input_file_path).suffix[1:]

    if format == ".pdf":
        process_book(input_file_path)
    else:
        result = convertapi.convert(
            "pdf", {"File": f"{input_file_path}"}, from_format=f"{format}"
        ).save_files(r"D:\Личные\books")

        return process_book(result[0])
