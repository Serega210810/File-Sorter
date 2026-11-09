import os
import shutil
from pathlib import Path

CATEGORIES = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Videos":    [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Music":     [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".pptx"],
}


def get_category(file_extension):
    ext = file_extension.lower()  
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category  
    return "Other"  


# === ГЛАВНЫЙ ЦИКЛ ПРОГРАММЫ ===
while True:
    print("\n" + "=" * 50)
    print("Программа сортировки файлов")
    print("=" * 50)

    # --- Ввод пути к папке ---
    folder_path = input("Введите путь к папке для сортировки: ").strip()

    # Проверка на пустой ввод
    if folder_path.strip() == "": #заменил на более читабельный вариант
        print("❌ Путь не может быть пустым! Попробуйте снова.")
        continue  

    folder = Path(folder_path)

    # --- Проверка существования папки ---
    if not folder.exists():
        print("❌ Указанная папка не существует. Проверьте путь и попробуйте снова.")
        continue  

    # --- Проверка, что путь ведёт именно к папке ---
    if not folder.is_dir():
        print("❌ Указанный путь не является папкой. Проверьте путь и попробуйте снова.")
        continue

    # --- Подсчёт файлов в папке ---
    files_count = 0
    for item in folder.iterdir(): #заменил на более читабельный вариант с помощью цикла for
        if item.is_file():
            files_count += 1
    print(f"\n📁 Найдено файлов: {files_count}")

    if files_count == 0:
        print("⚠ В папке нет файлов для сортировки.")
        again_question = input("\n🔄 Хотите попробовать другую папку? (да/нет): ").strip().lower() 
        if again_question != "да": #чуть заменил название переменной для лучшего понимания кода
            print("\n👋 Спасибо за использование программы!")
            break
        continue  

    # === ВЫБОР КАТЕГОРИЙ ДЛЯ СОРТИРОВКИ ===
    print("\n📋 Доступные категории:")
    categories_list = []
    for item in CATEGORIES.keys():
        print(f"   {item}")
        categories_list.append(item)
    for i in range(1, len(categories_list) + 1): 
        print(f"   {i}. {categories_list[i - 1]}") 
    print(f"   {len(categories_list) + 1}. Все категории") #Сделал более понятный цикл с использованием range

    # --- Ввод выбора ---
    choice = input("\nВыберите категории для сортировки (через запятую, например: 1,3,5): ").strip()

    # --- Обработка выбора ---
    if choice == str(len(categories_list) + 1):
        # Выбраны все категории
        selected_categories = set(categories_list)
    else:
        # Парсим числа через запятую
        try:
            indices = [int(x.strip()) for x in choice.split(",")]
            selected_categories = set()
            for idx in indices:
                if 1 <= idx <= len(categories_list):
                    selected_categories.add(categories_list[idx - 1])
                else:
                    print(f"⚠ Неверный номер: {idx}. Пропускаю.")
            
            if not selected_categories:
                print("❌ Не выбрано ни одной категории. Попробуйте снова.")
                continue
                
        except ValueError:
            print("❌ Некорректный ввод. Используйте числа через запятую.")
            continue

    print(f"\n✓ Выбраны категории: {', '.join(sorted(selected_categories))}")

    # --- Подтверждение перед сортировкой ---
    confirm = input(f"\nНачать сортировку файлов в папке '{folder_path}'? (да/нет): ").strip().lower()
    if confirm != "да":
        print("⏸ Сортировка отменена пользователем.")
        again = input("\n🔄 Хотите попробовать другую папку? (да/нет): ").strip().lower()
        if again != "да":
            print("\n👋 Спасибо за использование программы!")
            break
        continue

    # === ШАГ 1: СБОР НУЖНЫХ КАТЕГОРИЙ (первый проход) ===
    needed_categories = set()
    for item in folder.iterdir():
        if item.is_file():
            category = get_category(item.suffix)
            if category in selected_categories:  # Только выбранные категории
                needed_categories.add(category)

    # === ШАГ 2: СОЗДАНИЕ ТОЛЬКО НУЖНЫХ ПАПКА ===
    print("\n📂 Создаём папки категорий...")
    for category in needed_categories:
        category_folder = folder / category
        category_folder.mkdir(exist_ok=True)
        print(f"   ✓ Создана папка: '{category}'")

    # === ШАГ 3: ОПРЕДЕЛЕНИЕ НЕИСПОЛЬЗОВАННЫХ КАТЕГОРИЙ ===
    unused_categories = selected_categories - needed_categories

    # === ИНИЦИАЛИЗАЦИЯ СЧЁТЧИКОВ ===
    moved_count = 0     
    skipped_count = 0   
    error_count = 0     

    # === ОСНОВНОЙ ЦИКЛ СОРТИРОВКИ (второй проход) ===
    print("\n🔄 Начинаем сортировку...\n")
    for item in folder.iterdir():
        if item.is_file():  
            category = get_category(item.suffix)

            # Пропускаем файлы невыбранных категорий
            if category not in selected_categories:
                continue

            category_folder = folder / category
            destination = category_folder / item.name

            if destination.exists():
                print(f"⚠ Пропущен: '{item.name}' — файл уже есть в '{category}'")
                skipped_count += 1
                continue  

            try:
                shutil.move(str(item), str(destination))
                print(f"✓ Перемещён: '{item.name}' → '{category}'")
                moved_count += 1
            except Exception as e:
                print(f"✗ Ошибка при перемещении '{item.name}': {e}")
                error_count += 1

    # === ИТОГОВАЯ СТАТИСТИКА ===
    print("\n" + "=" * 50)
    print("✅ Сортировка завершена!")
    print(f"   📦 Перемещено: {moved_count}")
    print(f"   ⏭  Пропущено:  {skipped_count}")
    print(f"   ❌ Ошибок:     {error_count}")
    print("=" * 50)

    # === ВЫВОД НЕИСПОЛЬЗОВАННЫХ КАТЕГОРИЙ ===
    if unused_categories:
        print("\n📭 Папки для следующих ВЫБРАННЫХ категорий НЕ были созданы (нет файлов):")
        for category in sorted(unused_categories):
            print(f"   • {category}")
    else:
        print("\n🎉 Все выбранные категории оказались полезны!")

    # === ВОПРОС О ПРОДОЛЖЕНИИ ===
    again = input("\n🔄 Хотите отсортировать ещё одну папку? (да/нет): ").strip().lower()
    if again != "да":
        print("\n👋 Спасибо за использование программы! До свидания!")
        break
#Made by https://github.com/Serega210810