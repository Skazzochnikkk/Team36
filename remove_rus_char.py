'''import os
import re

# Путь к папке, в которой находятся файлы
#folder_path = r'C:\Users\Admin\Desktop\CPC\all_img'

# Функция для удаления русских символов из строки
def remove_russian_chars(input_str):
    # Шаблон для поиска русских символов
    russian_chars_pattern = re.compile('[а-яА-Я]')

    # Заменяем русские символы на пустую строку
    clean_str = re.sub(russian_chars_pattern, 'a', input_str)

    return clean_str


def remove_char(folder_path):
    # Перечисляем файлы в папке
    for filename in os.listdir(folder_path):
        # Получаем полный путь к файлу
        file_path = os.path.join(folder_path, filename)
        # Проверяем, является ли это файлом

        #буквы а-я без ё
        if os.path.isfile(file_path):
            # Удаляем русские символы из имени файла
            new_filename = remove_russian_chars(filename)

            # Формируем новый полный путь к файлу
            new_file_path = os.path.join(folder_path, new_filename)
            try:
                # Переименовываем файл
                os.rename(file_path, new_file_path)
            except:
                print("мы в говне")
                print('os')

'''