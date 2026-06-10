import os
import sys
import argparse

def clean_system(target_directory, rm_files=False, rm_dirs=False):
    print(f"Початок сканування директорії: {target_directory}\n")
    
    empty_files = []
    empty_dirs = []

    # Рекурсивний обхід папок знизу вгору (topdown=False),
    # щоб порожні папки, які містили порожні папки, видалялися коректно
    for root, dirs, files in os.walk(target_directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                    empty_files.append(file_path)
            except Exception:
                continue

        for directory in dirs:
            dir_path = os.path.join(root, directory)
            try:
                if os.path.isdir(dir_path) and not os.listdir(dir_path):
                    empty_dirs.append(dir_path)
            except Exception:
                continue

    # Виведення інформації про знайдене сміття
    print(f"Знайдено порожніх файлів (0 байт): {len(empty_files)}")
    for f in empty_files:
        print(f"  [ФАЙЛ] {f}")

    print(f"\nЗнайдено порожніх каталогів: {len(empty_dirs)}")
    for d in empty_dirs:
        print(f"  [ПАПКА] {d}")

    # Якщо прапорці видалення не передані — це режим Dry-run (сканування)
    if not rm_files and not rm_dirs:
        print("\n[Режим сканування (Dry-run)]. Жодних файлів не було видалено.")
        print("Для видалення використовуйте прапорці --rm-files та/або --rm-dirs.")
        return

    # Запит підтвердження у користувача перед деструктивною дією
    print("\nУВАГА! Ви збираєтеся видалити знайдені об'єкти.")
    confirmation = input("Ви впевнені, що хочете продовжити? (yes/no): ").strip().lower()
    if confirmation != 'yes':
        print("Операцію скасовано користувачем.")
        return

    # Видалення файлів
    if rm_files and empty_files:
        print("\nВидалення порожніх файлів...")
        for f in empty_files:
            try:
                os.remove(f)
                print(f"  Видалено: {f}")
            except Exception as e:
                print(f"  Помилка видалення файлу {f}: {e}")

    # Видалення папок
    if rm_dirs and empty_dirs:
        print("\nВидалення порожніх папок...")
        for d in empty_dirs:
            try:
                os.rmdir(d)
                print(f"  Видалено: {d}")
            except Exception as e:
                print(f"  Помилка видалення папки {d}: {e}")

    print("\nПроцес очищення завершено успішно.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для очищення системи від порожніх файлів та папок.")
    parser.add_argument("path", nargs="?", default=".", help="Шлях до цільової директорії (за замовчуванням поточна)")
    parser.add_argument("--rm-files", action="store_true", help="Видалити знайдені порожні файли")
    parser.add_argument("--rm-dirs", action="store_true", help="Видалити знайдені порожні каталоги")

    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Помилка: Шлях '{args.path}' не існує.")
        sys.exit(1)
        
    clean_system(args.path, rm_files=args.rm_files, rm_dirs=args.rm_dirs)
