from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Загрузка модели
model = load_model('PobedaV2.h5')  # модель качеста
model_ea = load_model('PobedaEA.h5')  # модель классов...

def model_check (img_path):
    # Загрузка изображения
    try:
        image = load_img(img_path, target_size=(768, 1024))  # Замените на путь к вашему изображению
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    # Преобразование изображения в numpy массив
    image = img_to_array(image)

    # Расширение размерности массива для совместимости с моделью
    image = np.expand_dims(image, axis=0)

    # Нормализация данных
    image = image / 255.0

    # Использование модели для предсказания на новых данных
    predictions = model.predict(image)

    print(predictions)
    if predictions>=0.4:
        return 0
    else:
        return 1


def model_check_ea (img_path):
    # Загрузка изображения
    try:
        image = load_img(img_path, target_size=(768, 1024))  # Замените на путь к вашему изображению
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    # Преобразование изображения в numpy массив
    image = img_to_array(image)

    # Расширение размерности массива для совместимости с моделью
    image = np.expand_dims(image, axis=0)

    # Нормализация данных
    image = image / 255.0

    # Использование модели для предсказания на новых данных
    predictions = model_ea.predict(image)

    print(predictions)
    #доопределить предсказания
    if (np.argmax(predictions) == 0):
        print("Парнокопытные")
        print(img_path)
        return 0, 1

    elif (np.argmax(predictions) == 1):
        print("Птицы")
        print(img_path)
        return 0, 1

    elif (np.argmax(predictions) == 2):
        print("Пустота")
        print(img_path)
        return 1, 0
    elif (np.argmax(predictions) == 3):
        print("Н/A")
        print(img_path)
        return 0, 1
    else:
        print("Warning wrong prediction")
        print(img_path)
        return -1, -1
    '''if predictions>=0.5:
        return 0
    else:
        return 1'''

#model_check_ea(r"C:\Users\Admin\Desktop\CPC\test\empty\clear_17.JPG")