import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

def get_file_mode(path):
    if path.is_symlink():
        return 'l'
    elif path.is_dir():
        return 'd'
    return '-'

def list_directory(directory_path, long_format=False, show_all=False):
    try:
        target_dir = Path(directory_path)
        if not target_dir.exists():
            print(f"Помилка: Шлях '{directory_path}' не існує.")
            return
        if not target_dir.is_dir():
            print(f"Помилка: Шлях '{directory_path}' не є директорією.")
            return

        try:
            items = list(target_dir.iterdir())
        except PermissionError:
            print(f"Помилка: Немає доступу до директорії '{directory_path}'.")
            return

        if not show_all:
            items = [item for item in items if not item.name.startswith('.')]

        items.sort(key=lambda x: x.name.lower())

        if long_format:
            print(f"{'Тип/Права':<10} {'Розмір (байт)':<15} {'Дата модифікації':<20} {'Назва':<s}")
            print("-" * 65)
            for item in items:
                try:
                    stats = item.stat()
                    size = stats.st_size if item.is_file() else 0
                    mtime = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    mode = get_file_mode(item)
                    print(f"{mode:<10} {size:<15} {mtime:<20} {item.name}")
                except Exception:
                    print(f"{'?':<10} {'?':<15} {'?':<20} {item.name} (Помилка доступу до метаданих)")
        else:
            for item in items:
                print(item.name)

    except Exception as e:
        print(f"Виникла непередбачувана помилка: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Аналог утиліти dir/ls на Python.")
    parser.add_index = False
    parser.add_argument("path", nargs="?", default=".", help="Шлях до каталогу (за замовчуванням поточний)")
    parser.add_argument("-l", "--long", action="store_true", help="Детальний формат виведення")
    parser.add_argument("-a", "--all", action="store_true", help="Показувати приховані файли")

    args = parser.parse_args()
    list_directory(args.path, long_format=args.long, show_all=args.all)
