import shutil
from pathlib import Path
import re
import sys

# Тут створюються кортежі з розширеннями для різних типів файлів
images_tuple = ('.jpeg', '.png', '.jpg', '.svg')
video_tuple = ('.avi', '.mp4', '.mov', '.mkv')
dokument_tuple = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
audio_tuple = ('.mp3', '.ogg', '.wav', '.amr')
archive_tuple = ('.zip', '.gz', '.tar')
sorting_folders = ('archives', 'video', 'audio', 'documents', 'images', 'unknown type')

# Словник трансляції для транслітерації кирилиці у латиницю за допомогою Unicode
TRANS = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D',
         1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I',
         1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N',
         1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T',
         1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch',
         1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y',
         1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je',
         1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'}

# Функція для рекурсивного видалення порожніх папок
def clean_fun(path):  
    p = Path(path)
    for folder in p.iterdir():
        if folder.name not in sorting_folders:
            if folder.is_dir():
                clean_fun(folder)
                if not any(folder.iterdir()):
                    folder.rmdir()

# Функція для нормалізації імен файлів та папок
def normalize(path):
    p = Path(path)
    for file_or_folder in p.iterdir():
        if file_or_folder.name == 'unknown type':
            continue
        if file_or_folder.is_dir():
            new_name = file_or_folder.name
            # Тут застосовується транслітерація та заміна неприпустимих символів на '_' для папки
            new_name = new_name.translate(TRANS)
            new_name = re.sub(r'\W', '_', new_name)
            new_path = file_or_folder.parent / new_name
            file_or_folder.rename(new_path)
            normalize(new_path)
        elif file_or_folder.is_file():
            new_name = file_or_folder.name.replace(file_or_folder.suffix, '')
            # Тут також застосовується транслітерація та заміна неприпустимих символів на '_' для файлу
            new_name = new_name.translate(TRANS)
            new_name = re.sub(r'\W', '_', new_name)
            new_name += file_or_folder.suffix
            new_path = file_or_folder.parent / new_name
            if new_path != file_or_folder:
                file_or_folder.rename(new_path)
                normalize(new_path)

# Функція для створення папок  та для сортування файлів
def create_folders(path, folder_list=sorting_folders):  
    for folder in folder_list:
        folder_path = Path(path) / folder
        folder_path.mkdir(exist_ok=True)

# Функція для розархівування архівів
def dearchives_func(file_name, path): 
    path_to_unpack = f'{path}/archives/'
    folder_path = Path(path_to_unpack) / Path(file_name).name.replace(Path(file_name).suffix, '')
    folder_path.mkdir(exist_ok=True)
    if file_name.suffix == '.zip':
        shutil.unpack_archive(file_name, folder_path, format='zip')
    elif file_name.suffix == '.tar':
        shutil.unpack_archive(file_name, folder_path, format='tar')
    elif file_name.suffix == '.gz':
        shutil.unpack_archive(file_name, folder_path, format='gz')

# Функція для сортування файлів
def sorted_func(file_name):  
    if file_name.suffix in dokument_tuple:  # Перевірка чи файл входить до документів 9 рядок
        target_folder = f'{my_path}/documents/'
        try:
            shutil.move(str(file_name), target_folder)
        except PermissionError:
            print(f'Помилка пов\'язана з тим, що файл {file_name.name} - відкритий !!!')
    elif file_name.suffix in images_tuple:  # Перевірка чи файл входить до картинок
        target_folder = f'{my_path}/images/'
        try:
            shutil.move(str(file_name), target_folder)
        except PermissionError:
            print(f'Помилка пов\'язана з тим, що файл {file_name.name} - відкритий !!!')  
    elif file_name.suffix in video_tuple:  # Перевірка чи файл входить до відео
        target_folder = f'{my_path}/video/'
        try:
            shutil.move(str(file_name), target_folder)
        except PermissionError:
            print(f'Помилка пов\'язана з тим, що файл {file_name.name} - відкритий !!!')
    elif file_name.suffix in audio_tuple:  # Перевірка чи файл входить до аудіо
        target_folder = f'{my_path}/audio/'
        try:
            shutil.move(str(file_name), target_folder)
        except PermissionError:
            print(f'Помилка пов\'язана з тим, що файл {file_name.name} - відкритий !!!')
    elif file_name.suffix in archive_tuple: # Перевірка чи файл входить до архівів 11 рядок
        dearchives_func(file_name, my_path)
    else:
        target_folder = f'{my_path}/unknown type/'
        shutil.move(str(file_name), target_folder)

# Рекурсивна функція для обходу файлів та сортування
def parser_func(path):
    p = Path(path)

    for items in p.iterdir():
        if items.name in sorting_folders:
            continue
        if items.is_dir():
            parser_func(items)
        elif items.is_file():
            sorted_func(items)
        print(items.name)


my_path = sys.argv[1]

# Основна функція, яка керує усім процесом тобто викликаємо у ній попередні функції
def main():  
    if len(sys.argv) < 2:
        print("Введіть в терміналі: python main.py <ваш шлях до папки з якою працюємо>")
        sys.exit(1)

    create_folders(my_path)
    parser_func(my_path)
    normalize(my_path)
    clean_fun(my_path)
    print(f"Вашу папку {my_path} відсортовано!")

# Виконання основної функції при запуску скрипта
if __name__ == '__main__':
    main()

