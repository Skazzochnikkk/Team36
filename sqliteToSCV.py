import sqlite3
import csv

def BDtoSCV(conn):
    # Подключение к базе данных SQLite
    cursor = conn.cursor()

    # SQL-запрос для выбора данных из базы данных
    select_query = """SELECT photo_name, defet_p ,empty_p, animal_p FROM photos"""

    # Выполнение SQL-запроса
    cursor.execute(select_query)

    # Получение результатов
    results = cursor.fetchall()

    # Закрытие соединения с базой данных
    conn.close()

    # Создание CSV-файла и запись данных
    with open("submission.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")

        # Запись заголовков столбцов (опционально)
        csv_writer.writerow(["filename", "broken", "empty", "animal"])

        # Запись данных
        for row in results:
            csv_writer.writerow(row)

    print("Успешно")