import os #Взаимодействие с ОС
import sqlite3 as sql #БД
import cv2 #OpenCV
import numpy as np
#функции со сторонних файлов
#import remove_rus_char # удалить
import model_implemintation
import sqliteToSCV
import shutil #копирование файлов

# нахождение путей со стартовой папки
def find_jpg_files(start_folder):
    jpg_files = []  # Список для хранения найденных файлов
    start_folder = os.path.abspath(start_folder)  # Преобразование в абсолютный путь

    # Обход всех папок и файлов внутри стартовой папки
    for foldername, subfolders, filenames in os.walk(start_folder):
        for filename in filenames:
            if filename.lower().endswith('.jpg'):
                # Определение пути относительно стартовой папки
                relative_path = os.path.relpath(foldername, start_folder)
                jpg_files.append(os.path.join(relative_path, filename))

    return jpg_files


#все загнали в функцию
def main_prog(folder_dir):

	#создание папок


	connection = sql.connect('my_database.db') #Создаем подключение к базе данных

	try:
		cur = connection.cursor()
		cur.execute("DROP TABLE IF EXISTS photos") #подключить когда проект реализован
		connection.commit()
		cur.execute("CREATE TABLE IF NOT EXISTS photos (photo_name STRING, width INT, height INT, defet_p INT, empty_p INT, animal_p, UNIQUE (photo_name))")
		connection.commit()
	except Exception as err:
		print('Таблица не создана')

	#folder_dir = r"C:\Users\Admin\Desktop\CPC\all_img" #Путь до католога

	'''remove_rus_char.remove_char(folder_dir)'''#удаляем русские символы из названия файлов (заменяем)

	short_paths = find_jpg_files(folder_dir)

	folder_path1 = folder_dir + "\\broken"
	folder_path2 = folder_dir + "\\empty"
	folder_path3 = folder_dir + "\\animal"
	os.makedirs(folder_path1)
	os.makedirs(folder_path2)
	os.makedirs(folder_path3)

	# проверить заполнение еще раз
	#перебор всех файлов в папке для определения их по типам
	for short_P in short_paths: #Получить список файлов в директории/каталоге
		'''if (images.endswith(".jpg") or images.endswith(".JPG")): #Проверка заканчивается ли название на png или jpg или jpeg'''
		'''print(images) #Печать названия'''
		img_dir=folder_dir+"\\"+short_P

		'''#получаем название файла
		if short_paths.rfind('/'):  # Проверяем, найдено ли вхождение '/'
			result = short_paths[:short_paths.rfind('/')]  # Используем срез для получения части строки до '/'
		else:
			result = short_paths'''

		# отсев изображений на плохие-хорошие
		defet = model_implemintation.model_check(img_dir)
		try:
			#данные с картинки
			stream = open(img_dir, 'rb')
			bytes = bytearray(stream.read())
			array = np.asarray(bytes, dtype=np.uint8)
			img = cv2.imdecode(array, cv2.IMREAD_UNCHANGED)

			#img = cv2.imread("C:\\Users\\Admin\\Desktop\\CPC\\all_img\\"+images)
			cur = connection.cursor()
			if int(defet)==1:
				cur.execute("INSERT OR REPLACE INTO photos (photo_name, width, height, defet_p, empty_p, animal_p) VALUES (?,?,?,?,?,?)",(short_P, img.shape[0], img.shape[1], int(defet), 0, 0))
				connection.commit()
				shutil.copy(img_dir, folder_path1)
			else:
				cur.execute("INSERT OR REPLACE INTO photos (photo_name, width, height, defet_p) VALUES (?,?,?,?)",(short_P, img.shape[0], img.shape[1], int(defet)))
				connection.commit()
		except KeyboardInterrupt:
			if int(defet) == 1:
				cur.execute("INSERT OR REPLACE INTO photos (photo_name, width, height, defet_p, empty_p, animal_p) VALUES (?,?,?,?,?,?)",(short_P, img.shape[0], img.shape[1], int(defet), 0, 0))
				connection.commit()
				shutil.copy(img_dir, folder_path1)
			else:
				cur.execute("INSERT OR REPLACE INTO photos (photo_name, width, height, defet_p) VALUES (?,?,?,?)",(short_P, img.shape[0], img.shape[1], int(defet)))
				connection.commit()
		except Exception as err:
			print('Добавляемое значение не добавленно в '+short_P)

	#промежуточный код
	my_list = []
	cur.execute("SELECT photo_name FROM photos WHERE defet_p = 0")
	rows = cur.fetchall()

	#преобразование текста
	for row in rows:
		start_index = str(row).find("'") + 1  # Находим индекс первой одинарной кавычки и добавляем 1
		end_index = str(row).rfind("'") # Находим индекс последней одинарной кавычки

		trimmed_string = str(row)[start_index:end_index]
		trimmed_string = trimmed_string.replace('\\', '', 1)
		my_list.append(trimmed_string)

	#перебор оставшихся значений
	for img_ea in my_list:
		img_dir_ea = folder_dir+"\\"+str(img_ea)
		# отсев изображений на плохие-хорошие
		Empty, animal = model_implemintation.model_check_ea(img_dir_ea)
		try:
			# данные с картинки
			stream = open(img_dir_ea, 'rb')
			bytes = bytearray(stream.read())
			array = np.asarray(bytes, dtype=np.uint8)
			img = cv2.imdecode(array, cv2.IMREAD_UNCHANGED)

			# img = cv2.imread("C:\\Users\\Admin\\Desktop\\CPC\\all_img\\"+images)
			cur = connection.cursor()
			if int(Empty) == 0 and int(animal) == 1:
				query=f"UPDATE photos SET empty_p = 0, animal_p = 1 WHERE photo_name = \'{img_ea}\'"
				cur.execute(query)
				connection.commit()
				shutil.copy(img_dir_ea, folder_path3)
			else:
				query = f"UPDATE photos SET empty_p = 1, animal_p = 0 WHERE photo_name = \'{img_ea}\'"
				cur.execute(query)
				connection.commit()
				shutil.copy(img_dir_ea, folder_path2)
		except KeyboardInterrupt:
			if int(Empty) == 0 and int(animal) == 1:
				query = f"UPDATE photos SET empty_p = 0, animal_p = 1 WHERE photo_name = \'{img_ea}\'"
				cur.execute(query)
				connection.commit()
				shutil.copy(img_dir_ea, folder_path3)
			else:
				query = f"UPDATE photos SET empty_p = 1, animal_p = 0 WHERE photo_name = \'{img_ea}\'"
				cur.execute(query)
				connection.commit()
				shutil.copy(img_dir_ea, folder_path2)
		except Exception as err:
			print('Добавляемое значение не добавленно в ' + str(img_ea))
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(err).__name__, err.args)
			print(message)


	sqliteToSCV.BDtoSCV(connection)
	connection.close()  # Закрытие подключения


print("END")

